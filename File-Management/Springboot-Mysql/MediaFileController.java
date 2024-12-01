package com.springboot.mysql.controller;

import java.io.IOException;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import com.springboot.mysql.entity.MediaFile;
import com.springboot.mysql.service.MediaService;

@RestController
@CrossOrigin
@RequestMapping("/media")
public class MediaFileController {
	
	@Autowired private MediaService mediaservice;
	
	@PostMapping("/upload")
	public ResponseEntity<String> uploadFile(@RequestParam("file") MultipartFile file,@RequestParam("title") String title){
		try {
			MediaFile mediaFile=mediaservice.saveFile(file,title);
			return new ResponseEntity<>("File uploaded successfully"+mediaFile.getId(),HttpStatus.OK);
		}
		catch(IOException e) {
			return  new ResponseEntity<>("File uploaded Failed",HttpStatus.INTERNAL_SERVER_ERROR);
		}
	}
	
	@GetMapping("/download/{id}")
	public ResponseEntity<byte[]> getFile(@PathVariable long id){
		Optional<MediaFile> mfo=mediaservice.getFile(id);
		if(mfo.isPresent()) {
			MediaFile mf=mfo.get();
			String contentType=infer(mf.getTitle());
			return ResponseEntity.ok()
					.header(HttpHeaders.CONTENT_DISPOSITION,"attachment ; filename=\""+mf.getTitle()+"\"")
					.contentLength(mf.getSize())
					.body(mf.getFileData());
		}
		else {
			return new ResponseEntity<>(HttpStatus.NOT_FOUND);
		}
	}
	
	private String infer(String fn) {
		String contentType="application/octet-stream";
		if(fn.endsWith(".jpg") || fn.endsWith(".jpeg")) contentType="image/jpeg";
		else if(fn.endsWith(".pdf")) contentType="application/pdf";
		else if(fn.endsWith(".mp4")) contentType="video/mp4";
		return contentType;
	}

}
