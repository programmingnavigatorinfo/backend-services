package com.spring_mongo.Spring_Mongo.service;

import com.spring_mongo.Spring_Mongo.entity.Item;
import com.spring_mongo.Spring_Mongo.repository.ItemRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;


@Service
public class ItemService {

    @Autowired
    private ItemRepository repository;

    // Fetch all items
    public List<Item> getAllItems() {
        return repository.findAll();
    }

    // Fetch an item by ID
    public Optional<Item> getItemById(String id) {
        return repository.findById(id);
    }

    // Save an item
    public Item saveItem(Item item) {
        return repository.save(item);
    }

    // Delete an item by ID
    public void deleteItemById(String id) {
        repository.deleteById(id);
    }
}