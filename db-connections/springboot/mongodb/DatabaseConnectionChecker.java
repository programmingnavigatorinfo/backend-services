package com.mydbconnect.MongoDBConnect;

import com.mongodb.MongoClientException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.stereotype.Component;

@Component
public class DatabaseConnectionChecker implements CommandLineRunner {

    @Autowired
    private MongoTemplate mongoTemplate;

    @Override
    public void run(String... args) {
        try {
            // Attempt to connect to the database
            mongoTemplate.getDb().getName(); // Will throw an exception if not connected
            System.out.println("MongoDB Connected successfully!");
        } catch (MongoClientException e) {
            System.err.println("MongoDB Connection failed: " + e.getMessage());
        }
    }
}