package com.spring_mongo.Spring_Mongo.repository;

import org.bson.types.ObjectId;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import com.spring_mongo.Spring_Mongo.entity.MediaFile;

@Repository
public interface MediaFileRepository extends MongoRepository<MediaFile,ObjectId>{

}
