#!/bin/sh
#
#     Created from:
#         SNMP Printer Check
#         check_snmp_printer
#         Version 3.141592 (December 12, 2011)
#         Authored by Jason Leonard
#         E-mail: jason_leonard@yahoo.com
#
#     Copyright (C) 2012 Savoir-Faire Linux Inc. 
#
#     This program is free software; you can redistribute it and/or modify 
#     it under the terms of the GNU General Public License as published by 
#     the Free Software Foundation; either version 3 of the License, or 
#     (at your option) any later version. 
#
#     This program is distributed in the hope that it will be useful, 
#     but WITHOUT ANY WARRANTY; without even the implied warranty of 
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
#     GNU General Public License for more details. 
#
#     You should have received a copy of the GNU General Public License 
#     along with this program; if not, write to the Free Software 
#     Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA. 
#
#     Projects :
#               SFL Shinken plugins
#
#     File :
#               check_snmp_printer.inc Check printer consumables status
#
#
#     Author: Thibault Cohen <thibault.cohen@savoirfairelinux.com> 
#


#############################################
#                                           #
#    Variables                              #
#                                           #
#############################################
PROGNAME=`basename $0`
PROGPATH=`echo $0 | sed -e 's,[\\/][^\\/][^\\/]*$,,'`
REVISION="0.1"


#############################################
#                                           #
#    Print Help                             #
#                                           #
#############################################
print_help(){
    print_revision $PROGNAME $REVISION
    echo ""
    print_usage
    echo ""
    support
    exit 0
}

#############################################
#                                           #
#    Print Usage                            #
#                                           #
#############################################

print_usage(){
    echo "Usage of $PROGNAME"
    echo " $PROGNAME -H <host/IP> -C <community> -x <check> [-w] [-c] [-S] | -h | -V "
    echo '---------------------------------------------------------------------'
    echo 'Usable Options:'
    echo '' 
    echo '   -C <community>'
    echo '       The SNMP Community variable - use the name of your SNMP community with read privileges'
    echo '       By default, the community is assumed to be public'
    echo '   -H <hostname>'
    echo '   (required option)'
    echo '       The IP address or hostname of the system to check'
    echo '   -S <text string>'
    echo '       assign a particular string as the separator for consumables.'
    echo '       Default is " " to conform to Nagios plugin development guidelines'
    echo '   -w <warn>'
    echo '       warning threshold (% of consumable remaining)'
    echo '       default 20'
    echo '   -c <crit>'
    echo '       critical threshold (% of consumable remaining)'
    echo '       default 5'
    echo '   -h'
    echo '       show this help screen'
    echo '   -V'
    echo '       show the current version of the plugin'
    echo '   -x <check>'     
    echo '   (required option)'
    echo '       The check you want to perform for the printer. Choose from the following:'
    echo ''
    echo '           CONSUM {<string> | TEST | ALL}'
    echo '               <string> will give you all consumables matching the string '
    echo "                  For example, 'CONSUM Toner' will only show toner levels"
    echo '               TEST will give you the exact names of available consumables'
    echo '                   For example,'
    echo '                       Black Toner Cartridge HP C4191A'
    echo '                   To monitor a consumable, call the function as follows:'
    echo "                      $PROGNAME -H <hostname> -C <community> -x \"CONSUM Black\" "
    echo '               ALL gives you all consumable output at once.'
    echo ''
    echo '           CONSUMX <string>'
    echo '                  this gives you results only for the ***EXACT*** consumable specified by <string>'
    echo '                       For example, '
    echo '                            CONSUMX "Black Toner Cartridge" '
    echo '                       will only give you the usage for a consumable named "Black Toner Cartridge". '
    echo '                       It will not give you results for "Black Toner Cartridge 1" or "Black Toner". '
    echo '           DISPLAY'
    echo '                  Report contents of printer display'
    echo ''
    echo '           DEVICES'
    echo '                  Status of hardware modules'
    echo ''
    echo '           MESSAGES'
    echo '                  Event logs reported by the printer'
    echo ''
    echo '           MODEL'
    echo '                  ALL will give you all tray output at once.'
    echo ''
    echo '           PAGECOUNT'
    echo '                  How many pages this printer has processed (culmulative)'
    echo ''
    echo '           STATUS'
    echo '                  Overall status of the printer'
    echo ''
    echo '           TRAY {<number> | TEST | ALL}'
    echo '                  <number> will give you output for the specified tray. A comma-separated list of values is possible as well.'
    echo "                  TEST will give you the #'s of all trays available "
    echo '                  ALL will give you all tray output at once.'
    echo ''
    echo 'Examples:'
    echo "    $PROGNAME -H 10.0.1.10 -C public -x \"CONSUM ALL\" -w 25 -c 10 "
    echo "    $PROGNAME -H 10.0.1.10 -C public -x \"CONSUMX Punch Dust Box\" "
    echo "    $PROGNAME -H 10.0.1.10 -C public -x MODEL "
    echo "    $PROGNAME -H 10.0.1.10 -C public -x \"TRAY 2,3\" "
    echo "    $PROGNAME -V"
    echo ''
    echo '---------------------------------------------------------------------'
}

#############################################
#                                           #
#    Check arguments validity               #
#                                           #
#############################################

check_arguments(){
    if [ -z "$host_name" ]
    then
        echo "Hostname option is missing"
        print_help
        exit 3
    fi

    if [ -z "$community" ]
    then
        community="public"
    fi

    if [ -z "$port" ]
    then
        port="161"
    fi

    if [ -z "$version" ]
    then
        version="2c"
    fi

    if [ -z "$separator" ]
    then
        separator=" "
    fi

    if [ -z "$warning" ]
    then
        warning=20
    fi

    if [ -z "$critical" ]
    then
        critical=5
    fi

}

#############################################
#                                           #
#    Get data and prepare output            #
#                                           #
#############################################
get_data(){
    all_markers=$(snmpwalk -v $version -On -c $community $host_name:$port 1.3.6.1.2.1.43.11.1.1.6.1 2>/dev/null)
    if [ $? -ne 0 ]; then
        #Check for server response - is SNMP even setup okay?
        echo "WARNING: No SNMP response from $host_name! Make sure host is up and SNMP is configured properly."
        exit 3
    else
        string_type=$(echo "$all_markers" | tr -d "\n" | cut -d " " -f3)
        case "$check" in
            "MESSAGES")
                check_messages
                ;;
            "MODEL")
                check_model
                ;;
            "CONSUM")
                check_consumables "$parameter"
                ;;
            "CONSUMX")
                check_exact_consumable "$parameter"
                ;;
            "TRAY")
                check_paper_trays "$parameter"
                ;;
            "PAGECOUNT")
                check_page_count
                ;;
            "DEVICES")
                check_device_status
                ;;
            "STATUS")
                check_printer_status
                ;;
            "DISPLAY")
                check_display
                ;;
            *) # no parameters were passed, or a parameter was incorrect (wrong spelling, etc.)
                echo 'Invalid check specified by -x parameter.'
                echo ''
                print_help
                exit 3
                ;;
        esac
        return $?
    fi
}


#########################################################
##         check_model function                        ##
#########################################################
# Returns printer model and serial. Always returns OK   #
#########################################################

check_model(){
#   Vendor specific items to code here!
#       possibly serial #
    model=$(snmpget -Ovq -v $version -c $community $host_name:$port 1.3.6.1.2.1.25.3.2.1.3.1 2>/dev/null)
    serial=$(snmpwalk -Ovq -v $version -c $community $host_name:$port 1.3.6.1.2.1.43.5.1.1.17 2>/dev/null | tr -d "\"")

    exit_string="$model, Serial # $serial"
    return 0
}


#########################################################
##        check_messages function                      ##
#########################################################
# Shows messages on the printer display. The OID is not #
# commonly used in all printers                         #
#########################################################

check_messages(){
    messages=$(snmpwalk -Ovq -v $version -c $community $host_name:$port 1.3.6.1.2.1.43.18.1.1.8 2>/dev/null | tr -d "\"" | tr "\n" "\!")
    if [ -z "$messages" ]; then
        exit_string="UNKNOWN: Can't determine messages. Device does not support this OID.\n"
        return 3
    else
        exit_string="$messages"
    fi

    return 0

}


#########################################################
##       check_page_count function                     ##
#########################################################
# Returns pretty-formatted page count for the printer.  #
# Awesome for tracking historical page usage.           #
#########################################################

check_page_count(){
    page_count=$(snmpget -Ovq -v $version -c $community $host_name:$port 1.3.6.1.2.1.43.10.2.1.4.1.1 2>/dev/null )
    exit_string="Pagecount is $page_count"
    perfdat="$page_count;;;0;"
    return 0
}


#########################################################
##        check_display function                       ##
#########################################################
#                                                       #
#########################################################

check_display(){
    display=$(snmpwalk -Ovq -v $version -c $community $host_name:$port 1.3.6.1.2.1.43.16.5.1.2.1 2>/dev/null | tr -d "\"" )
    # if display is null, we need to let the user know
    if [ $? -eq 0 ]; then
        # Let's make sure we eliminate any extra new lines, or at least replace them with our
        #   specified SEPARATOR (which could be a new line)
        exit_string=$(echo "$display" | tr "\n" "$separator")
        return 0
    else
        # Something happened or this OID isn't available
        exit_string="UNKNOWN - printer does not appear to support using this OID."
        return 3
    fi

}


#########################################################
##          check_printer_status function              ##
#########################################################
#                                                       #
#########################################################

check_printer_status(){
    exit_code=0
    printer_status=$(snmpget -Ovq -v $version -c $community $host_name:$port 1.3.6.1.2.1.25.3.5.1.1.1 2>/dev/null)
    case "$printer_status" in
        other|other\(1\)|1)
            exit_string="CRITICAL: Printer status is other(1)"
            exit_code=2
        ;;
        idle|idle\(3\)|3)
            exit_string="OK: Printer status is idle(3)"
        ;;
        printing|printing\(4\)|4)
            exit_string="OK: Printer status is printing(4)"
        ;;
        warmup|warmup\(5\)|5)
            exit_string="OK: Printer status is warmup(5)"
        ;;
        *)
            exit_string="WARNING: Printer status is unknown: $printer_status"
            exit_code=1
        ;;
    esac

    return $exit_code
}


#########################################################
##      check_device_status function                   ##
#########################################################
#                                                       #
#########################################################

check_device_status(){

    current_exit_code=0
    current_status=0
    device_status=""
    device_name=""
    device_ids=$(snmpwalk -On -v $version -c $community $host_name:$port 1.3.6.1.2.1.25.3.2.1.1 2>/dev/null)

    # create this around a for loop on id's, which come from .1.3.6.1.2.1.25.3.2.1.1.x
    for id in $(echo $device_ids | egrep -oe '[[:digit:]]+\ =' | cut -d " " -f1)
    do
        device_name=$(snmpget -Ovq -v $version -c $community $host_name:$port 1.3.6.1.2.1.25.3.2.1.3.$id 2>/dev/null)
        exit_string="$exit_string$device_name status is "

        device_status=$(snmpget -Ovq -v $version -c $community $host_name:$port 1.3.6.1.2.1.25.3.2.1.5.$id 2>/dev/null)

        case "$device_status" in
            unknown|unknown\(1\)|1)
                exit_string="${exit_string}Status : Unknown(1) - WARNING!$separator"
                current_status=1
            ;;
            running|running\(2\)|2)
                exit_string="${exit_string}Status : running(2) - OK!$separator"
                current_status=0
            ;;
            warning|warning\(3\)|3)
                exit_string="${exit_string}Status : warning(3) - WARNING!$separator"
                current_status=1
            ;;
            testing|testing\(4\)|4)
                exit_string="${exit_string}Status : testing(4) - OK!$separator"
                current_status=0
            ;;
            down|down\(5\)|5)
                exit_string="${exit_string}Status : down(5) - CRITICAL!$separator"
                current_status=2
            ;;
            *)
                exit_string="${exit_string}Status : Unknow($device_status) - WARNING!$separator"
                current_status=1
            ;;
        esac

        if [ "$current_status" -gt "$current_exit_code" ]; then
            current_exit_code="$current_status"
        fi

    done

    return $current_exit_code

}


#########################################################
##        check_one_consumable function                ##
#########################################################
# Given the marker's ID (1, 2, 3, etc.), this function  #
# grabs the consmable string for that ID, converts it   #
# to a name and determines capacity and status code for #
# it.                                                   #
#                                                       #
# Only status code is returned. Global string variables #
# are used for printing and other functionality.        #
#########################################################

check_one_consumable () {

    local consum_exit_code=0
    current_capacity=0
    max_capacity=0
    marker_name=""
    marker_color=""
    marker_string=$(snmpget -On -v $version -c $community $host_name:$port 1.3.6.1.2.1.43.11.1.1.6.1.$1 2>/dev/null)

    # We'll be parsing our name differently depending on whether we have Hex-String or not
    if [ "$string_type" = "Hex-STRING:" ]; then
        marker_name=$(echo "$marker_string" | cut -d ":" -f2- | tr -d "\n" | xxd -r -p)
    else
        marker_name=$(echo "$marker_string" | cut -d " " -f4- | tr -d "\"")
    fi

    # Some manufacturers don't put the actual cartridge color in the above OID text for 
    #   MARKER_STRING. Instead, each entry just says "toner". The OID used here is 
    #   a place where an associated color string must be stored. We are going to get this 
    #   info. and use it if not already available in the MARKER_NAME we've parsed.
    # --- Thanks to Martin <8a>oltis for letting me know about this problem on some copiers.
    getcolor=$(snmpget -v $version -c $community $host_name:$port 1.3.6.1.2.1.43.12.1.1.4.1.$1 2>/dev/null)
    marker_color=$(echo $getcolor | cut -d " " -f4- | tr -d "\"")

    # We're just checking here to see if the consumable already has this color in its text description
    if [ $(echo "$marker_name" | grep -vqi "$marker_color") ]; then
        # It doesn't, so we're going to add it
        marker_name="$marker_color $marker_name"
    fi

    # As usual, if the results are an empty set, something went wrong or didn't match up
    if [ -z "$marker_name" ]; then
        exit_string="UNKNOWN - OID not found! Your printer may not support checking this consumable."
        exit_string="$exit_string Use the CONSUM TEST option to determine which consumables may be monitored."
        perfdat=""
        consum_exit_code=3
    else
        # Determine capacities for the current marker
        current_capacity=$(snmpget -Ovq -v $version -c $community $host_name:$port 1.3.6.1.2.1.43.11.1.1.9.1.$1 2>/dev/null)
        max_capacity=$(snmpget -Ovq -v $version -c $community $host_name:$port 1.3.6.1.2.1.43.11.1.1.8.1.$1 2>/dev/null)
        if [ "$max_capacity" -lt 0 ]; then
            max_capacity=0
        fi

        # the component does not have a measurable status indication
        case "$current_capacity" in
            "-3") # A value of (-3) means that the printer knows that there is some supply/remaining space
                exit_string="$exit_string$marker_name is OK!$separator"
            ;;
            "-2") # The value (-2) means unknown
                exit_string="$exit_string$marker_name is at WARNING level!$separator"
                if [ "$consum_exit_code" -lt 1 ]; then
                    consum_exit_code=1
                fi
            ;;
            "0") # Something is empty!
                exit_string="$exit_string$marker_name is at CRITICAL level!$separator"
                consum_exit_code=2
            ;;
            *) # A positive value means this is a measurable component - let's report it's status code and let user know the % usage
                current_capacity=$(( $current_capacity * 100 / $max_capacity ))
                if [ "$current_capacity" -gt "$warning" ]; then
                    exit_string="$exit_string$marker_name is at $current_capacity%% - OK!$separator"
                else
                    if [ "$current_capacity" -le "$warning" ] && [ "$current_capacity" -gt "$critical" ]; then
                        exit_string="$exit_string$marker_name is at $current_capacity%% - WARNING!$separator"
                        if [ "$consum_exit_code" -lt 1 ]; then
                            consum_exit_code=1
                        fi
                    else
                        if [ "$current_capacity" -le "$critical" ]; then
                            exit_string="$exit_string$marker_name is at $current_capacity%% - CRITICAL!$separator"
                            consum_exit_code=2
                        fi
                    fi
                fi
                perfdat="$perfdat $marker_name=$current_capacity%%;$warning;$critical;0;100"
            ;;
        esac

    fi

    return $consum_exit_code

}


#########################################################
##        check_exact_consumable function              ##
#########################################################
# Loops through all consumables and compares the string #
# passed to the consumable string. If a match is found, #
# we calculate and output capacity and status. If a     #
# match is not found, let the user know.                #
#                                                       #
# Global string variables are used for printing status  #
# and perf data.                                        #
#########################################################

check_exact_consumable(){

    local consumx_exit_code=0
    found=false
    found_marker=0

    # Now we can loop through everything that matched
    for marker_id in $(echo "$all_markers" | egrep -oe '[[:digit:]]+\ =' | cut -d " " -f1)
    do
        marker_string=$(snmpget -On -v $version -c $community $host_name:$port 1.3.6.1.2.1.43.11.1.1.6.1.$marker_id 2>/dev/null)

        # We'll be parsing our name differently depending on whether we have Hex-String or not
        if [ "$string_type" = "Hex-STRING:" ]; then
            marker_name=$(echo "$marker_string" | cut -d ":" -f2- | tr -d "\n" | xxd -r -p)
        else
            marker_name=$(echo "$marker_string" | cut -d " " -f4- | tr -d "\"")
        fi

        # Update our boolean if we find a match!
        if [ "$1" = "$marker_name" ]; then
            found=true
            found_marker="$marker_id"
        fi
    done

    if $found; then
        # Determine capacities for the marker of the matching consumable
        x_current_capacity=$(snmpget -Ovq -v $version -c $community $host_name:$port 1.3.6.1.2.1.43.11.1.1.9.1.$found_marker 2>/dev/null)
        max_capacity=$(snmpget -Ovq -v $version -c $community $host_name:$port 1.3.6.1.2.1.43.11.1.1.8.1.$found_marker 2>/dev/null)
        if [ "$max_capacity" -lt 0 ]; then
            max_capacity=0
        fi

        # the component does not have a measurable status indication
        case "$X_CURRENT_CAPACITY" in
            "-3") # A value of (-3) means that the printer knows that there is some supply/remaining space
                exit_string="$exit_string$1 is OK!\n"
            ;;
            "-2") # The value (-2) means unknown
                exit_string="$exit_string$1 is at WARNING level!$separator"
                if [ "$consumx_exit_code" -lt 1 ]; then
                    consumx_exit_code=1
                fi
            ;;
            "0") # Something is empty!
                exit_string="$exit_string$1 is at CRITICAL level!$separator"
                consumx_exit_code=2
            ;;
            *) # A positive value means this is a measurable component - let's report it's status code and let user know the % usage
                x_current_capacity=$(( $x_current_capacity * 100 / $max_capacity))

                if [ "$x_current_capacity" -gt "$warning" ]; then
                    exit_string="$exit_string$1 is at $x_current_capacity%% - OK!$separator"
                else
                    if [ "$x_current_capacity" -le "$warning" ] && [ "$x_current_capacity" -gt "$critical" ]; then
                        exit_string="$exit_string$1 is at $x_current_capacity%% - WARNING!$separator"
                        if [ "$consumx_exit_code" -lt 1 ]; then
                            consumx_exit_code=1
                        fi
                    else
                        if [ "$x_current_capacity" -le "$critical" ]; then
                            exit_string="$exit_string$1 is at $x_current_capacity%% - CRITICAL!$separator"
                            consumx_exit_code=2
                        fi
                    fi
                fi
                perfdat="$perfdat $1=$x_current_capacity;$warning;$critical;"
            ;;
        esac
    else
        # Let the user know we didn't find anything, and report back the string they sent. Also prompt them to run the TEST option to double-check their string
        exit_string="UNKNOWN - No match found for '$1'! Use the CONSUM TEST option to determine which consumables may be monitored."
        consumx_exit_code=3
    fi

    return $consumx_exit_code

}


#########################################################
##      check_consumables function                     ##
#########################################################
# Determines which consumables to check and then pass   #
# them all off to check_one_consumable                  #
#                                                       #
# Global string variables are used for printing status  #
# and perf data.                                        #
#########################################################

check_consumables(){

    local consums_exit_code=0
    hex_id=0
    current_status=0
    hex_marker=""
    ascii_marker=""
    markers_matched=""

    case "$1" in
        "TEST") # User passed "TEST" parameter - output what consumables are available
            printf "Consumables you may monitor:\n"

            if [ "$string_type" = "Hex-STRING:" ]; then
                for hex_id in $(echo "$all_markers" | egrep -oe '[[:digit:]]+\ =' | cut -d " " -f1)
                do
                    hex_marker=$(snmpget -On -v $version -c $community $host_name:$port 1.3.6.1.2.1.43.11.1.1.6.1.$hex_id 2>/dev/null)
                    ascii_marker=$(echo "$hex_marker" | cut -d ":" -f2 | tr -d "\n" | xxd -r -p)
                    exit_string="$exit_string$ascii_marker\n"
                done
            else
                exit_string=$(snmpwalk -Ovq -v $version -c $community $host_name:$port 1.3.6.1.2.1.43.11.1.1.6.1 2>/dev/null)
            fi

            consums_exit_code=3
        ;;
        "ALL") # User passed ALL parameter - check everything!
            # Let's loop through all consumables available
            for marker_id in $(echo "$all_markers" | egrep -oe '[[:digit:]]+\ =' | cut -d " " -f1)
            do
                check_one_consumable "$marker_id"
                current_status=$?

                if [ "$current_status" -gt "$consums_exit_code" ]; then
                    consums_exit_code="$current_status"
                fi
            done
        ;;
        *) # A string was passed, on which we will match to available consumable strings
            if [ "$string_type" = "Hex-STRING:" ]; then
                # If our printer uses Hex-STRING fields, we need to convert our user's string to hex first
                hex_string=$(echo "$1" | tr -d "\n" | xxd -p -u)

                # Now that we have a hex string for the user string, we need look for it in output that is formatted similarly 
                #   XXD -p doesn't output spaces, but the Hex-STRING fields do use spaces between each byte
                markers_matched=$(echo "$all_markers" | tr -d " " | egrep -i "$hex_string")
            else
                markers_matched=$(echo "$all_markers" | egrep -i "$1")
            fi

            if [ -z "$markers_matched" ]; then
                exit_string="UNKNOWN - OID not found! Your printer may not support checking this consumable."
                echo "$exit_string Use the CONSUM TEST option to determine which consumables may be monitored."
                exit 3
            else
                # Now we can loop through everything that matched
                for marker_id in $(echo "$markers_matched" | cut -d "=" -f1 | cut -d "." -f14)
                do
                    check_one_consumable "$marker_id"

                    current_status=$?

                    if [ "$current_status" -gt "$consums_exit_code" ]; then
                        consums_exit_code="$current_status"
                    fi
                done
            fi
        ;;
    esac

    return $consums_exit_code

}


#########################################################
##        check_one_tray Function                      ##
#########################################################
# Checks the tray #, as passed by parameter. If found,  #
# it returns the status and capacity.                   #
#                                                       #
# Only status code is returned. Global string variables #
# are used for printing and other functionality.        #
#########################################################

check_one_tray (){

    tray_exit_code=0
    tray_capacity=0
    tray_max_capacity=0
    tray_feed_dimension=0
    tray_xfeed_dimension=0
    tray_dimension_units=0

    tray_capacity=$(snmpwalk -Ovq -v $version -c $community $host_name:$port 1.3.6.1.2.1.43.8.2.1.10.1.$1 2>/dev/null)
    if [ -z "$tray_capacity" -o "$tray_capacity" = "No Such Instance currently exists at this OID" ]; then
        exit_string="$exit_string UNKNOWN - Tray $1 not found. Use the TRAY TEST option to determine which trays may be monitored.\n"
        tray_exit_code=3
    else
        # Determine information about the tray
        tray_name=$(snmpwalk -Ovq -v $version -c $community $host_name:$port 1.3.6.1.2.1.43.8.2.1.13.1.$1 2>/dev/null)

        # Some manufacturers do not set the tray name OID, so we'll assume a generic name depending on the # passed to the function
        if [ "$tray_name"=="" ]; then
            tray_name="Tray $1"
        fi

        case "$tray_capacity" in
            "-3") # The value (-3) means that the printer knows that at least one unit remains.
                exit_string="$exit_string$tray_name is OK!$separator"
            ;;
            "-2") # The value (-2) means unknown
                exit_string="$exit_string$tray_name status is UNKNOWN!$separator"
                tray_exit_code=3
            ;;
            "0") # 0 means there is no paper left! This is our only critical value.
                # Determine paper size of current tray
                tray_feed_dimension=$(snmpwalk -Ovq -v $version -c $community $host_name:$port 1.3.6.1.2.1.43.8.2.1.4.1.$1 2>/dev/null)
                tray_xfeed_dimension=$(snmpwalk -Ovq -v $version -c $community $host_name:$port 1.3.6.1.2.1.43.8.2.1.5.1.$1 2>/dev/null)
                tray_dimension_units=$(snmpwalk -Ovq -v $version -c $community $host_name:$port 1.3.6.1.2.1.43.8.2.1.3.1.$1 2>/dev/null)

                if [ "$tray_feed_dimension" -lt 0 ] && [ "$tray_xfeed_dimension" -lt 0 ]; then
                    # If either dimension was negative, then we really don't know much about the dimension
                    tray_dimension_string="paper."
                else

                    case "$tray_dimension_units" in
                        "3") # convert ten thousandths of an inch to inches
                        tray_feed_dimension=$(echo "scale=1;$tray_feed_dimension/10000" | bc)
                        tray_xfeed_dimension=$(echo "scale=1;$tray_xfeed_dimension/10000" | bc)
                        ;;
                        "4") # convert micrometers to inches, and get the int portion
                        tray_feed_dimension=$(echo "scale=1;$tray_feed_dimension*0.0000393700787" | bc)
                        tray_feed_dimension=$(echo "scale=1;$tray_feed_dimension+0.5" | bc)
                        tray_feed_dimension=$(echo "scale=1;$tray_feed_dimension/1" | bc)

                        tray_xfeed_dimension=$(echo "scale=1;$tray_xfeed_dimension*0.0000393700787" | bc)
                        tray_xfeed_dimension=$(echo "scale=1;$tray_xfeed_dimension+0.5" | bc)
                        tray_xfeed_dimension=$(echo "scale=1;$tray_xfeed_dimension/1" | bc)
                        ;;
                    esac

                    tray_dimension_string="$tray_xfeed_dimension x $tray_feed_dimension paper."
                fi

                exit_string="$exit_string$tray_name is at CRITICAL level - please refill with more $tray_dimension_string$separator"
                tray_exit_code=2
            ;;
            *) # A positive number indicates how many pages are left. We'll calculate what % of capacity this is and determine status
                tray_max_capacity=$(snmpwalk -Ovq -v $version -c $community $host_name:$port 1.3.6.1.2.1.43.8.2.1.9.1.$1 2>/dev/null )
                tray_capacity=$(( $tray_capacity * 100 / $tray_max_capacity))

                if [ "$tray_capacity" -gt "$critical" ]; then
                    exit_string="$exit_string$tray_name is at $tray_capacity%% - OK!$separator"
                else
                    if [ "$tray_capacity" -le "$warning" ]; then
                        # Determine paper size of current tray
                        tray_feed_dimension=$(snmpwalk -Ovq -v $version -c $community $host_name:$port 1.3.6.1.2.1.43.8.2.1.4.1.$1 2>/dev/null )
                        tray_xfeed_dimension=$(snmpwalk -Ovq -v $version -c $community $host_name:$port 1.3.6.1.2.1.43.8.2.1.5.1.$1 2>/dev/null )
                        tray_dimension_units=$(snmpwalk -Ovq -v $version -c $community $host_name:$port 1.3.6.1.2.1.43.8.2.1.3.1.$1 2>/dev/null )
                        if [ "$tray_feed_dimension" -lt 0 ] && [ "$tray_xfeed_dimension" -lt 0 ]; then
                            # If either dimension was negative, then we really don't know much about the dimension
                            tray_dimension_string="paper."
                        else
                            case "$tray_dimension_units" in
                                "3") # convert ten thousandths of an inch to inches
                                tray_feed_dimension=$(echo "scale=1;$tray_feed_dimension/10000" | bc)
                                tray_xfeed_dimension=$(echo "scale=1;$tray_xfeed_dimension/10000" | bc)
                                ;;
                                "4") # convert micrometers to inches, and get the int portion
                                tray_feed_dimension=$(echo "scale=1;$tray_feed_dimension*0.0000393700787" | bc)
                                tray_feed_dimension=$(echo "scale=1;$tray_feed_dimension+0.5" | bc)
                                tray_feed_dimension=$(echo "scale=1;$tray_feed_dimension/1" | bc)

                                tray_xfeed_dimension=$(echo "scale=1;$tray_xfeed_dimension*0.0000393700787" | bc)
                                tray_xfeed_dimension=$(echo "scale=1;$tray_xfeed_dimension+0.5" | bc)
                                tray_xfeed_dimension=$(echo "scale=1;$tray_xfeed_dimension/1" | bc)
                                ;;
                            esac

                            tray_dimension_string="$tray_xfeed_dimension x $tray_feed_dimension paper."
                        fi

                        if [ "$tray_capacity" -le "$critical" ]; then
                            # we have a critical: we already know the value is less than warning
                            exit_string="$exit_string$tray_name is at $tray_capacity%% - CRITICAL! Please refill with more $tray_dimension_string$separator"
                            tray_exit_code=2
                        else
                            # we are only below warning, but not yet below critical
                            exit_string="$exit_string$tray_name is at $tray_capacity%% - WARNING! Please refill with more $tray_dimension_string$separator"
                            if [ "$tray_exit_code" -lt 1 ]; then
                                tray_exit_code=1
                            fi
                        fi
                    fi
                fi
                perfdat="$perfdat $tray_name=$tray_capacity;$warning;$critical;"
            ;;
        esac

    fi

    return $tray_exit_code

}

#########################################################
##      check_paper_trays Function                     ##
#########################################################
# Determines which trays to check and passes each check #
# off to check_one_tray.                                #
#                                                       #
# Global string variables are used for printing status  #
# and perf data.                                        #
#########################################################

check_paper_trays (){

    trays_exit_code=0
    all_trays=$(snmpwalk -On -v $version -c $community $host_name:$port 1.3.6.1.2.1.43.8.2.1.10.1 2>/dev/null)
    current_tray_status=0

    case "$1" in
        "TEST")
            echo "Trays you may monitor:"
            echo "$(echo "$all_trays" | egrep -oe '[[:digit:]]+\ =' | cut -d " " -f1)"
            trays_exit_code=3
        ;;
        "ALL") # let's check all trays!
            for tray_id in $(echo "$all_trays" | egrep -oe '[[:digit:]]+\ =' | cut -d " " -f1)
            do
                check_one_tray "$tray_id"
                current_tray_status=$?

                if [ "$current_tray_status" -gt "$trays_exit_code" ]; then
                    trays_exit_code="$current_tray_status"
                fi
            done
        ;;
        *)
            for tray_id in $(echo "$1" | tr "$arg_token" "\n")
            do
                check_one_tray "$tray_id"
                current_tray_status=$?

                if [ "$current_tray_status" -gt "$trays_exit_code" ]; then
                    trays_exit_code="$current_tray_status"
                fi
            done
        ;;
    esac

    return $trays_exit_code

}

