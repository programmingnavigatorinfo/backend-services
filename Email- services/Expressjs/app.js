const express=require("express")
const nodemailer=require("nodemailer")


const app=express()

const port= 4200

const transporter = nodemailer.createTransport({
    host:"smtp.gmail.com",
    port:465,
    secure:true,
    auth:{
        user:"your email",
        pass:"your password"
    }
})


app.use(express.json())

app.post("/send-email",async(req,res)=>{
    const {to,subject,text}=req.body;

    try{
        const mailOptions={
            from:"Your Name <your email>",
            to,
            subject,
            text,
        };

        await transporter.sendMail(mailOptions);
        res.status(200).json({message:"email sent successfully"});
    }

    catch(error){
        res.status(500).json({error:"failed"})
    }
})

app.listen(port,()=>{
    console.log("server is running");
})
