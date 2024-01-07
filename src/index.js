
const fetch=require('node-fetch')
const express=require('express');
const bodyParser=require('body-parser')
const cora=require('cors')
const helmet=require('helmet')
const http=require('https')
const app=express()
app.use(bodyParser.json());
app.use(cora())
app.use(bodyParser.urlencoded({extended:true}))
app.use(bodyParser.json())

app.post('/login',async(req,res)=>{
    const url="https://accounts.zoho.in/oauth/v2/token?refresh_token="+req.body.refresh_token+"&grant_type=refresh_token&client_id="+req.body.client_id+"&client_secret="+req.body.client_secret+"&redirect_uri==https://accounts.zoho.in"
        const tokenResponse=await fetch(url,{
            method:"POST"
        })
        console.log("Refresh Token")
        const data = await tokenResponse.json();
    res.send(data)
})

app.post('/request',async (req,res)=>{
    //console.log(req.body.input_data)
   const inputData=JSON.stringify(req.body.input_data)
   console.log(inputData)
    const body=new URLSearchParams({input_data:inputData})
    const headers={
        'Content-Type':'application/x-www-form-urlencoded',
        'authorization':req.headers.authorization,
        'accept':req.headers.accept
    }
   // console.log(headers)
    let response=await fetch("https://sdpondemand.manageengine.in/api/v3/requests",{
        method:"POST",
        body:body,
        headers:headers
    })
    const resData=await response.json()
    res.send(resData)
})

app.listen(3000,()=>{

})
