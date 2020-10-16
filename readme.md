# GustelDDNS - README

# Currently supported Launch parameters:

Command | Description
--------|------------
-new | Creates domain **locally**, it has to exist on the CloudFlare Server
-update | updates locally created Domains on Cloudflare Server

## How to use

Requirements:
- CloudFlare xAuthKey and E-Mail
- Existing A-Record (AAAA is not Supported)


1. Start Program with parameter -new to create record.
2. Update as DDNS marked records by starting the program with -update


## Planned Changes
- [ ] Catching possible exceptions
- [ ] *maybe* making it a Service
- [ ] GUI(?)

## DISCLAIMER
As you can obvously can see, I have no idea how to code.
I would not recommend using this code for anything if you don't expect it do break randomly.
