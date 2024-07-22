from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Ipdevices
from .models import db
import json, os

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    
    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash('Note deleted successfully', category='success')
    return jsonify({})
    #return render_template("note.html", user=current_user)  


@views.route('/note', methods=['GET', 'POST'])
@login_required
def note_add():
    if request.method == 'POST':
        note = request.form.get('note')
        
        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    return render_template("note.html", user=current_user)


@views.route('/ipDevices', methods =['GET', 'POST'])
@login_required
def ipDevices_status():
    if request.method == 'POST':
        ipAddr = request.form.get('ipAddress')
        ipNam = request.form.get('ipName')

        ipexist = Ipdevices.query.filter_by(ipaddress =ipAddr).first()

        if ipexist:
            flash('IP Address alreaddy exist', category='error')

        elif len(ipAddr) =='':
            flash('IP addresss can not be empty', category='error')
        elif len(ipNam) == '':
            flash('IP Address name cannot be empty', category='error')
        else:
            new_ip =Ipdevices(ipaddress =ipAddr, ipname =ipNam, ipstatus = ipNam)
            db.session.add(new_ip)
            db.session.commit()
            flash('IP Devices successfully added', category='success')
   
    data_ip = Ipdevices.query.all()
    status=''
    #for ip in data_ip:
    #    ip1 = ip.ipaddress
    #    responce = os.popen("ping " + ip1).read()
    #    if 'Received = 4' in responce:
    #        status = 'Online'
    #    else:
    #        status='Offline' 
    return render_template('devices.html', user=current_user, data_ip= data_ip ,status=status)



@views.route('/delete-ip-device', methods =['POST'])
def delete_ip_device():
    ipaddr = json.loads(request.data)
    idaddrID = ipaddr['ipId']
    ipaddre = Ipdevices.query.get(idaddrID)
    if ipaddre:
        db.session.delete(ipaddre)
        db.session.commit()
        flash('IP Device deleted successfully', category='success')
    return jsonify({})

