const express=require('express')
const request=require('request')

const app=express()

const API="be73c793a2bce7f8830ad7bc329aace9"


app.get('/',(req,res)=>{
    let city=req.query.city;

    if(!city){
        return res.send("please enter city using query params");
    }

    request(
        `https://api.openweathermap.org/data/2.5/weather?q=${city}&units=metric&appid=${API}`,
        (error,response,body)=>{
            const data=JSON.parse(body);
            if(response.statusCode==200) {res.send(data);}
            else {res.send("error in fetching");}
        }
    )


})

app.listen(3000,()=>{
    console.log("server is running");
})
