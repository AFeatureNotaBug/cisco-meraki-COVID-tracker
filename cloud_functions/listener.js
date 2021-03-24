/**
 * Responds to any HTTP request.
 *
 * @param {!express:Request} req HTTP request context.
 * @param {!express:Response} res HTTP response context.
 */
 const admin = require('firebase-admin');
admin.initializeApp();
exports.helloWorld = async(req, res) => {
  await admin.firestore().collection('logs').add({"info":req.headers})
  if (req.method === 'GET'){
  res.status(200).send("ciscoVerificationKey");
  }else{
    if(req.body!= undefined && req.body.key != undefined){
      if(req.body.key == 'usersecret'){
        r = await admin.firestore().collection('cisco').orderBy('createdAt','desc').get()
        res.status(200).send(r.docs[0].data())
      }else{
        res.send(401).send('Not authorized')
      }

    }else{
      var d = Date.now()
      r = await admin.firestore().collection('cisco').orderBy('createdAt').get()
      r.docs[0].ref.update({"body":req.body,"createdAt":d})
    }
  res.status(200).send('done')
  }
};