package com.springboot.mysql.service;

import java.io.IOException;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import com.springboot.mysql.entity.MediaFile;
import com.springboot.mysql.repository.MediaFileRepository;

@Service
public class MediaService {

	@Autowired private MediaFileRepository mediafielrepo;

	public MediaFile saveFile(MultipartFile file, String title) throws IOException {
		
		MediaFile mediaFile=new MediaFile();
		mediaFile.setTitle(title);
		mediaFile.setSize(file.getSize());
		mediaFile.setFileData(file.getBytes());
		return mediafielrepo.save(mediaFile);
	}

	public Optional<MediaFile> getFile(long id) {
		return mediafielrepo.findById(id);
	}
	
}
