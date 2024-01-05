console.log('Hello There!')

const express=require('express');
const bodyParser=require('body-parser')
const cora=require('cors')
const helmet=require('helmet')
const morgan=require('morgan')

const http=require('https')
const app=express()
app.use(bodyParser.json());
app.use(cora())
app.use(bodyParser.urlencoded({extended:true}))
app.use(bodyParser.json())


app.get('/dummy',(req,res)=>{
    console.log(req.body)
    res.send("Success")
})

app.post('/request',async (req,res)=>{
    const body=new URLSearchParams({input_data:req.body.input_data})
   // console.log(body)
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
    let output={}
    if(response.status==401)
    {
        const url="https://accounts.zoho.in/oauth/v2/token?refresh_token="+req.body.refresh_token+"&grant_type=refresh_token&client_id="+req.body.client_id+"&client_secret="+req.body.client_secret+"&redirect_uri=https://accounts.zoho.in"
        const tokenResponse=await fetch(url,{
            method:"POST"
        })
        console.log("Refresh Token")
        const data = await tokenResponse.json();
        headers.authorization="Zoho-oauthtoken "+data.access_token
        response=await fetch("https://sdpondemand.manageengine.in/api/v3/requests",{
        method:"POST",
        body:body,
        headers:headers
    })
    output['AUTHORIZATION']=data
    }
    const resData=await response.json()
    output['REQUEST']=resData
    res.send(output)
})

app.listen(30001,()=>{

})