from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from flask import send_file

from .auth import login_required
from .db import get_db
import os

bp = Blueprint("account", __name__)
import sys
sys.path.insert(0, '../client') # For relative import
from encrypt import generatePEM, loadKeys, generateCert, verify, loadCert

pub_path = "./keys/public_test.pem"
pv_path = "./keys/private_test.pem"
cert_path = "./certs/cert.pem"
uuid_example = "6e604468-5eea-44c7-947a-86a5b3125411"
@bp.route("/account")
@login_required
def index():
    db = get_db()
    id = g.user['id']
    # generatePEM(pub_key_path=pub_path, pv_key_path=pv_path)
    # generateCert(public_key=pub_path, private_key=pv_path, location="./certs/cert.pem")
    # verify(cert=cert_path, public_key=pub_path)
    # loadCert(cert_path)
    certs = db.execute(
        "SELECT c.id, name, description, serial_number, valid, expires, uuid"
        " FROM cert c JOIN user u ON c.user_id = u.id"
        f" WHERE user_id = {id} "
        " ORDER BY valid DESC"
    ).fetchall()


    # print(certs)
    # for x in certs: 
    #     print(x['name'])

    
    return render_template("account/index.html", certs=certs)


@bp.route("/<int:id>/download")
@login_required
def downloadFile(id):
    user_id = g.user['id']
    db = get_db()
    file = db.execute(
        "SELECT cert_path"
        " FROM cert c JOIN user u ON c.user_id = u.id"
        f" WHERE user_id = {user_id} "
    ).fetchall()
    path = os.path.abspath(file[0]['cert_path'])
    return send_file(path)

@bp.route("/<int:id>/create", methods=("POST", ))
@login_required
def create(id):  
    print(f"ID: {id}")
    db = get_db()
    path = f"./certs/{id}/"
    full_path = path + "cert.pem"
    if((os.path.exists(path)) == 0):
        print("Path does not exist")
        os.mkdir(path)
    
    num_certs = len([c for c in os.listdir(path)])
    # print(f"Number of certs: {num_certs}")
    full_path = path + "cert" + "_" + str(num_certs) + ".pem"
    
        
    account = request.form["account"]
    name = request.form["name"]
    description = request.form["description"]
    ip = request.remote_addr
    
    print(f"Account: {account}")

    # Generate the certificate
    generateCert(pub_path, pv_path, location=full_path, uid=account, ip=ip)
    serial, uid, valid, expire = loadCert(full_path)
    serial = str(serial)
    if(verify(full_path, pub_path) == 1):
        print("Error: Verification Failed.")
        # need to do something if this happens (it shouldn't happen)
    
    print(f"Serial: {serial}")
    print(f"UID: {uid}")
    print(f"Valid: {valid}")
    print(f"Expire: {expire}")
    
    db.execute(
        "INSERT INTO cert (name, description, serial_number, uuid, valid, expires, ip, cert_path, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
        (name, description, serial, uid, valid, expire, ip, full_path, id)
    )
    db.commit()

    
    return redirect(url_for("account.index"))
    