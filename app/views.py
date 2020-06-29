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
        #removeLastOctet=request.form['removeLastOctet']
        #removeLastOctet=request.POST.get('removeLastOctet')

        if form.removeLastOctet.data:
            ipList = OrderedSet()
        else:
            ipList = list()

        if subnetsInput is not None:
            subnetList = subnetsInput.split()

            try:
                for subnet in subnetList:
                    for ip in ipaddress.IPv4Network(subnet):

                        if form.removeLastOctet.data:

                            # Remove last octet of IP
                            ip3 = separator.join(str(ip).split(separator, 3)[:-1])

                            # Add IP to list if not duplicate
                            ipList.add(ip3)

                        else:

                            # Return 4 octets
                            ipList.append(ip)

            except ValueError as e:
                flash('Please check the subnet format. All subnets must use the CIDR notation (e.g. 192.168.178.0/24).')
    
        if not form.validate():
            flash('Please enter one subnet per row.')
            
    return render_template('index.html', form=form, ipList=ipList)