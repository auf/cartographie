# ipaddresses.rb
# Try to get additional Facts about the machine's network interfaces
#
# Original concept Copyright (C) 2007 psychedelys <psychedelys@gmail.com>
# Update and *BSD support (C) 2007 James Turnbull <james@lovedthanlost.net>
#

require 'facter/util/ip'

ipaddresses = ''
Facter::Util::IP.get_interfaces.each do |interface|
    ip = Facter::Util::IP.get_interface_value(interface, 'ipaddress')
    if ip
      ipaddresses = ipaddresses + ',' + ip
    end 
end

Facter.add(:ipaddresses) do
  setcode do
    ipaddresses[1..-1]
  end 
end
