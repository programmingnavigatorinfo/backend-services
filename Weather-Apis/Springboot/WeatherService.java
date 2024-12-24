package com.springboot.mysql.service;

import java.io.IOException;

import org.json.JSONObject;
import org.springframework.stereotype.Service;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

@Service
public class WeatherService {
	
	private OkHttpClient client;
	private Response response;
	
	private String API="be73c793a2bce7f8830ad7bc329aace9";
	

	public JSONObject getWeather(String city) {
		client= new OkHttpClient();
		Request request= new Request.Builder().url("https://api.openweathermap.org/data/2.5/weather?q="+city+"&units=metric&appid="+API).build();
		
		try {
			response=client.newCall(request).execute();
			return new JSONObject(response.body().string());
		}
		
		catch(IOException e) {
			System.out.print("error");
			e.printStackTrace();
		}
		return null;
		
	}

}
