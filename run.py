from flask import *
from flask_pymongo import PyMongo
import pymongo
from bson.objectid import ObjectId
from datetime import date

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/data_library"
mongo = PyMongo(app)
collist = mongo.db.list_collection_names()
if 'membre' not in collist:
	mongo.db.create_collection('membre')
if 'livre' not in collist:
	mongo.db.create_collection('livre')
if 'historique' not in collist:
	mongo.db.create_collection('historique')
if 'user' not in collist:
	mongo.db.create_collection('user')

@app.route('/',methods=['GET','POST'])
@app.route('/login/',methods=['GET','POST'])
def login():
    err=False
    if request.method=='POST':
        nom=request.form['user']
        mdp=request.form['mdp']
        try:
            ex_user=mongo.db.user.find({'nom':nom,'mdp':mdp})[0]
            return redirect(url_for('accueil'))
        except:
            return render_template('login.html',err=True)
    return render_template('login.html')

@app.route('/inscrire/',methods=['GET','POST'])
def inscrire():
    err=False
    if request.method=='POST':
        nom=request.form['user']
        mdp=request.form['mdp']
        mdp2=request.form['mdp2']
        if mdp==mdp2 and mdp!='':
            mongo.db.user.insert_one({'nom':nom,'mdp':mdp})
            return redirect(url_for('accueil'))
        else:
            return render_template('inscrire.html',err=True)
    return render_template('inscrire.html')

@app.route('/mdp/',methods=['GET','POST'])
def modifier_mdp():
    err=False
    if request.method=='POST':
        nom=request.form['user']
        mdp=request.form['mdp']
        mdp1=request.form['mdp1']
        mdp2=request.form['mdp2']
        try:
            ex_user=mongo.db.user.find({'nom':nom})[0]
            if ex_user['mdp']==mdp:
                if mdp1==mdp2 and mdp1!='':
                    mongo.db.user.update_one(ex_user,{"$set":{'mdp':mdp1}})
                    return redirect(url_for('accueil'))
                else:
                    return render_template('mdp.html',err=True)
            else:
                return render_template('mdp.html',err=True)
        except:
            return render_template('mdp.html',err=False)
    return render_template('mdp.html')

@app.route('/accueil/')
def accueil():	
	return render_template('accueil.html')

@app.route('/livre/ajouter/',methods=['GET','POST'])
def ajouter_livre():	
    liv={}
    if request.method=='POST':
        nom=request.form['nom']
        categ=request.form['categ']
        auteur=request.form['auteur']
        nouv={'nom':nom,'categ':categ,'auteur':auteur}
        mongo.db.livre.insert_one(nouv)
        return redirect(url_for('livre_avec_notif',notif=1))	
    return render_template('livre_ajout.html',**locals())

@app.route('/livre/')
def livre():
	return redirect(url_for('livre_avec_notif',notif=0))

@app.route('/livre/<notif>/')
def livre_avec_notif(notif):
	list_livre=mongo.db.livre.find()
	return render_template('livre.html',**locals())

@app.route('/confirmer/<dom>/<id_supp>/')
def confirmer(dom,id_supp):
	return render_template('confirmer.html',**locals())

@app.route('/supprimer/<dom>/<id_supp>/')
def supprimer(dom,id_supp):
    q={'_id':ObjectId(id_supp)}
    if dom=='livre':
        mongo.db.livre.delete_one(q)
        return redirect(url_for('livre_avec_notif',notif=2))
    elif dom=='membre':
        mongo.db.membre.delete_one(q)
        return redirect(url_for('membre_avec_notif',notif=2))
    return redirect(url_for('livre_avec_notif',notif=2))

@app.route('/modifier_livre/<idl>/',methods=['GET','POST'])
def modifier_livre(idl):	
    q={'_id':ObjectId(idl)}
    liv=mongo.db.livre.find(q)[0]
    if request.method=='POST':
        nom=request.form['nom']
        categ=request.form['categ']
        auteur=request.form['auteur']
        nouv={"$set":{'nom':nom,'categ':categ,'auteur':auteur}}
        mongo.db.livre.update_one(liv,nouv)
        return redirect(url_for('livre_avec_notif',notif=3))	
    return render_template('livre_ajout.html',**locals())

@app.route('/membre/ajouter/',methods=['GET','POST'])
def ajouter_membre():	
    memb={}
    if request.method=='POST':
        num=request.form['num']
        nom=request.form['nom']
        prenom=request.form['prenom']
        adr=request.form['adr']
        tel=request.form['tel']
        nouv={'num':num,'nom':nom,'prenom':prenom,'adr':adr,'tel':tel,'date_adh':date.today().isoformat()}
        mongo.db.membre.insert_one(nouv)
        return redirect(url_for('membre_avec_notif',notif=1))	
    return render_template('membre_ajout.html',**locals())

@app.route('/membre/')
def membre():
	return redirect(url_for('membre_avec_notif',notif=0))

@app.route('/membre/<notif>/')
def membre_avec_notif(notif):
	list_membre=mongo.db.membre.find()
	return render_template('membre.html',**locals())

@app.route('/modifier_membre/<idl>/',methods=['GET','POST'])
def modifier_membre(idl):	
    q={'_id':ObjectId(idl)}
    memb=mongo.db.membre.find(q)[0]
    if request.method=='POST':
        num=request.form['num']
        nom=request.form['nom']
        prenom=request.form['prenom']
        adr=request.form['adr']
        tel=request.form['tel']
        nouv={"$set":{'num':num,'nom':nom,'prenom':prenom,'adr':adr,'tel':tel,'date_adh':date.today().isoformat()}}
        mongo.db.membre.update_one(memb,nouv)
        return redirect(url_for('membre_avec_notif',notif=3))	
    return render_template('membre_ajout.html',**locals())

@app.route('/pret/',methods=['GET','POST'])
def pret():
	memb=mongo.db.membre.find()
	liv=mongo.db.livre.find()
	if request.method=='POST':
		pnum=request.form['memb']
		pliv=request.form['liv']
		pj=request.form['j']
		nouv= {'pnum':pnum,'pliv':pliv,'pj':pj,'pdate':date.today().isoformat(),'rdate':None}
		mongo.db.historique.insert_one(nouv)
		return redirect(url_for('rendu',notif=1))
	return render_template('pr.html',**locals())

@app.route('/rendu/<notif>/')
def rendu(notif):
	q={'rdate':None}
	hist=mongo.db.historique.find(q)
	return render_template('rendu.html',**locals())

@app.route('/rendre/<pnum>/<pliv>/')
def rendre(pnum,pliv):
	q={'pnum':pnum,'pliv':pliv,'rdate':None}
	q2={"$set":{'rdate':date.today().isoformat()}}
	mongo.db.historique.update_one(q,q2)
	return redirect(url_for('historique',notif=1))	

@app.route('/historique/<notif>/')
def historique(notif):
	hist=mongo.db.historique.find()
	return render_template('historique.html',**locals())



if __name__ == "__main__":
    app.run(debug=True) 
