#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, abort, jsonify, make_response, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import aliased
from sqlalchemy.dialects.oracle import CHAR, NUMBER, VARCHAR2, DATE
from config import config

app = Flask(__name__)
app.config.from_object(config)
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

##############################

class Arinvt(db.Model):
    __tablename__ = 'arinvt'
    id = db.Column(NUMBER, primary_key=True)
    itemno = db.Column(CHAR)
    descrip = db.Column(CHAR)
    eplant_id = db.Column(NUMBER)
    standard_id = db.Column(NUMBER, db.ForeignKey('standard.id'))


class V_RT_Workorders(db.Model):
    __tablename__ = 'v_rt_workorders'
    workorder_id = db.Column(NUMBER, primary_key=True)
    standard_id = db.Column(NUMBER, db.ForeignKey('standard.id'))
    eqno = db.Column(CHAR)
    down_code = db.Column(CHAR)
    down_descrip = db.Column(CHAR)
    mfgcell = db.Column(CHAR)
    shift_rejects = db.Column(NUMBER)
    orig_dwn_st_time = db.Column(DATE)
    last_cycle = db.Column(NUMBER)


class Standard(db.Model):
    __tablename__ = 'standard'
    id = db.Column(NUMBER, primary_key=True)
    arinvt_id_mat = db.Column(NUMBER, db.ForeignKey('arinvt.id'))
    nuser3 = db.Column(NUMBER)


class Partno(db.Model):
    __tablename__ = 'partno'
    id = db.Column(NUMBER, primary_key=True)
    arinvt_id = db.Column(NUMBER, db.ForeignKey('arinvt.id'))
    standard_id = db.Column(NUMBER, db.ForeignKey('standard.id'))


##############################


@app.route('/realtime', methods=['GET'])
def realtime():
    res = db.session.query(V_RT_Workorders, Arinvt, Standard, Partno).\
            filter(V_RT_Workorders.standard_id == Standard.id).\
            filter(Standard.id == Partno.standard_id).\
            filter(Partno.arinvt_id == Arinvt.id).\
            filter(V_RT_Workorders.mfgcell == 'INJECTION').\
            filter(Arinvt.eplant_id == '1').all()

#     eqno = res.V_RT_Workorders.eqno.rstrip()
#     descrip = res.Arinvt.descrip.rstrip()
#     mfg_cycle = str(res.Standard.nuser3).rstrip()
#     last_cycle = str(res.V_RT_Workorders.last_cycle).rstrip()
#     down_code = str(res.V_RT_Workorders.down_code).rstrip()
#     down_descrip = str(res.V_RT_Workorders.down_descrip).rstrip()
#     shift_rejects = str(res.V_RT_Workorders.shift_rejects).rstrip()

    return render_template('index.html', res=res)

#     return jsonify({
#         'eqno': eqno,
#         'descrip': descrip,
#         'mfg_cycle': mfg_cycle,
#         'last_cycle': last_cycle,
#         'down_code': down_code,
#         'down_descrip': down_descrip,
#         'shift_rejects': shift_rejects
#     })



@app.route('/press/<int:press_id>', methods=['GET'])
def press(press_id):
    res = db.session.query(V_RT_Workorders, Arinvt).\
            filter(V_RT_Workorders.standard_id == Standard.id).\
            filter(Standard.id == Arinvt.standard_id).\
            filter(V_RT_Workorders.eqno == str(press_id)).\
          first() or abort(404)
    res2 = db.session.query(V_RT_Workorders, Arinvt).\
            filter(V_RT_Workorders.standard_id == Standard.id).\
            filter(Standard.arinvt_id_mat == Arinvt.id).\
            filter(V_RT_Workorders.eqno == str(press_id)).\
          first() or abort(404)

    press_id = res.V_RT_Workorders.eqno.rstrip()
    wo_id = str(int(res.V_RT_Workorders.workorder_id))
    itemno = res.Arinvt.itemno.rstrip()
    descrip = res.Arinvt.descrip.rstrip()
    itemno_mat = res2.Arinvt.itemno.rstrip()
    descrip_mat = res2.Arinvt.descrip.rstrip()
    return jsonify({'press_id': press_id,
                    'wo_id': wo_id,
                    'itemno': itemno,
                    'descrip': descrip,
                    'itemno_mat': itemno_mat,
                    'descrip_mat': descrip_mat})



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True) 
