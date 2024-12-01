package com.spring_mongo.Spring_Mongo.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import com.spring_mongo.Spring_Mongo.entity.MediaFile;
import com.spring_mongo.Spring_Mongo.repository.MediaFileRepository;

import org.bson.BsonBinarySubType;
import org.bson.types.Binary;
import org.bson.types.ObjectId;

import java.io.IOException;
import java.util.Optional;

@Service
public class MediaFileService {

    @Autowired
    private MediaFileRepository mediaFileRepository;

    public MediaFile saveFile(MultipartFile file, String title) throws IOException {
        MediaFile mediaFile = new MediaFile();
        mediaFile.setTitle(title);
        mediaFile.setSize(file.getSize());
        mediaFile.setFileData(new Binary(BsonBinarySubType.BINARY, file.getBytes()));
        return mediaFileRepository.save(mediaFile);
    }

    public Optional<MediaFile> getFile(String id) {
        ObjectId objectId;
        try {
            objectId = new ObjectId(id);
        } catch (IllegalArgumentException e) {
            return Optional.empty();
        }
        return mediaFileRepository.findById(objectId);
    }
}
