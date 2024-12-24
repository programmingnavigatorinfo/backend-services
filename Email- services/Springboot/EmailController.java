package com.springboot.mysql.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import com.springboot.mysql.entity.EmailRequest;
import com.springboot.mysql.service.EmailService;

@RestController
public class EmailController {
	
	@Autowired
	private EmailService es;
	
	@PostMapping("/send-email")
	public ResponseEntity<String> sendEmail(@RequestBody EmailRequest request){
		es.sendEmail(request.getTo(),request.getSubject(),request.getText());
		return ResponseEntity.ok("Email sent successfully");
	}

}
