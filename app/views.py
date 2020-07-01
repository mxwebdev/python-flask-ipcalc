from flask import render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, BooleanField
import ipaddress
from ordered_set import OrderedSet

from app import app

separator = "."

# App
class ReusableForm(Form):
    subnetsInput = TextAreaField('Subnet(s):', validators=[validators.required()], default="192.168.1.0/28\n10.10.0.0/24")
    removeLastOctet = BooleanField('Remove Last Octet')
    
@app.route("/", methods=['GET', 'POST'])
def index():
    form = ReusableForm(request.form)

    ipList = None
    
    if request.method == 'POST':
        subnetsInput=request.form['subnetsInput']

        #if form.removeLastOctet.data:
        ipList = OrderedSet()
        #else:
        #    ipList = list()

        if subnetsInput is not None:
            subnetList = subnetsInput.split()

            ipCount = 0
            subnetCount = 0

            try:

                # Check count of IPs within the given networks
                for subnet in subnetList:
                    ipCount = ipCount + ipaddress.IPv4Network(subnet).num_addresses
                    subnetCount = subnetCount + 1

                print(subnetCount)

                for subnet in subnetList:

                    if form.removeLastOctet.data and ipCount/256 <= 10000:
                        for ip in ipaddress.IPv4Network(subnet):
                            # Remove last octet of IP
                            ip3 = separator.join(str(ip).split(separator, 3)[:-1])
                            # Add IP to list if not duplicate
                            ipList.add(ip3)

                    elif ipCount <= 10000:
                        for ip in ipaddress.IPv4Network(subnet):
                        
                            # Return 4 octets
                            #ipList.append(ip)
                            ipList.add(ip)
                    else:
                        flash('The count of IPs resulting from your input would be too high (max. 10.000). Consider removing the last octet by clicking on the checkbox below to shorten your output.')
                        break

            except ValueError as e:
                flash('Please check the subnet format. All subnets must use the CIDR notation (e.g. 192.168.178.0/24).')
    
        if not form.validate():
            flash('Please enter one subnet per row.')
            
    return render_template('index.html', form=form, ipList=ipList)