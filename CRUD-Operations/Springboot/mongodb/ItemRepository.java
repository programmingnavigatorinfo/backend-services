package com.spring_mongo.Spring_Mongo.repository;


import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import com.spring_mongo.Spring_Mongo.entity.Item;


@Repository
public interface ItemRepository extends MongoRepository<Item, String> {

	}