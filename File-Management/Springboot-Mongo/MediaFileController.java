package com.spring_mongo.Spring_Mongo.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import com.spring_mongo.Spring_Mongo.entity.MediaFile;
import com.spring_mongo.Spring_Mongo.service.MediaFileService;

import java.io.IOException;
import java.util.Optional;

@RestController
@CrossOrigin
@RequestMapping("/media")
public class MediaFileController {

    @Autowired
    private MediaFileService mediaFileService;

    @PostMapping("/upload")
    public ResponseEntity<String> uploadFile(@RequestParam("file") MultipartFile file,
                                             @RequestParam("title") String title) {
        try {
            MediaFile mediaFile = mediaFileService.saveFile(file, title);
            return new ResponseEntity<>("File uploaded successfully: " + mediaFile.getId().toString(), HttpStatus.OK);
        } catch (IOException e) {
            return new ResponseEntity<>("Failed to upload file", HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @GetMapping("/download/{id}")
    public ResponseEntity<byte[]> getFile(@PathVariable String id) {
        Optional<MediaFile> mediaFileOptional = mediaFileService.getFile(id);
        if (mediaFileOptional.isPresent()) {
            MediaFile mediaFile = mediaFileOptional.get();
            String contentType = inferContentType(mediaFile.getTitle());
            return ResponseEntity.ok()
                    .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"" + mediaFile.getTitle() + "\"")
                    .contentLength(mediaFile.getSize())
                    .contentType(org.springframework.http.MediaType.parseMediaType(contentType))
                    .body(mediaFile.getFileData().getData());
        } else {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
    }

    private String inferContentType(String filename) {
        String contentType = "application/octet-stream";
        if (filename.endsWith(".jpg") || filename.endsWith(".jpeg")) {
            contentType = "image/jpeg";
        } else if (filename.endsWith(".png")) {
            contentType = "image/png";
        } else if (filename.endsWith(".gif")) {
            contentType = "image/gif";
        } else if (filename.endsWith(".pdf")) {
            contentType = "application/pdf";
        } else if (filename.endsWith(".mp4")) {
            contentType = "video/mp4";
        }
        return contentType;
    }
}
