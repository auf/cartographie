#!/bin/sh
#
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
#               check_snmp_printer.sh Check printer consumables status
#
#
#     Author: Thibault Cohen <thibault.cohen@savoirfairelinux.com> 
#
#


PROGPATH=`echo $0 | sed -e 's,[\\/][^\\/][^\\/]*$,,'`

if [ -e $PROGPATH/utils.sh ]
then
    . $PROGPATH/utils.sh
elif [ -e ./utils.sh ]
then
    . ./utils.sh
else
    echo "UNKNOWN : utils.sh not found"
    exit 1
fi

if [ -e $PROGPATH/check_snmp_printer.inc ]
then
    . $PROGPATH/check_snmp_printer.inc
elif [ -e ./check_snmp_printer.inc ]
then
    . ./check_snmp_printer.inc
else
    echo "UNKNOWN : check_snmp_printer.inc not found"
    exit 1
fi

#############################################
#                                           #
#    Return output and exit code            #
#                                           #
#############################################

while getopts "P:V:C:H:c:w:x:S:hv" opt;
do
    case "$opt" in
        C) # Assign community
            community="$OPTARG"
        ;;
        V) # Assign community
            version="$OPTARG"
        ;;
        P) # Assign community
            port="$OPTARG"
        ;;
        H) # Assign hostname
            host_name="$OPTARG"
        ;;
        x) # Assign check to perform
            check=$(echo "$OPTARG" | cut -d " " -f1)
            parameter=$(echo "$OPTARG" | cut -d " " -f2-)
        ;;
        S) # Assign separator
            separator="$OPTARG"
        ;;
        w)
            warning=$OPTARG
        ;;
        c)
            critical=$OPTARG
        ;;
        h)
            print_help
            exit 3
        ;;
        v)
            print_revision $PROGNAME $REVISION
            exit 3
        ;;
        \?)
            print_help
            exit 3
        ;;
        :)
            # maybe useless
            echo "Option -$OPTARG requires an argument." >&2
            print_help
        ;;
    esac

    
done

check_arguments

get_data
exit_code=$?


# If the program hasn't exited already, then a check was run okay and we can quit.
if [ "$perfdat" = "" ]; then
    printf "$exit_string\n"
else
    printf "$exit_string|$perfdat\n"
fi

exit $exit_code

