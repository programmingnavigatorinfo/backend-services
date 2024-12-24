package com.springboot.mysql.controller;

import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import com.springboot.mysql.service.WeatherService;

@RestController
@CrossOrigin
public class WeatherController {
	
	@Autowired
	WeatherService ws;
	
	@GetMapping(value="/weather/{city}",produces="application/json")
	public ResponseEntity<String> getData(@PathVariable String city){
		JSONObject obj = ws.getWeather(city);
		if(obj.length()>1) return new ResponseEntity<>(obj.toString(),HttpStatus.OK);
		else return new ResponseEntity<>("weather data not found",HttpStatus.NOT_FOUND);
	}

}
