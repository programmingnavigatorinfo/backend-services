package com.spring_mongo.Spring_Mongo.controller;

import com.spring_mongo.Spring_Mongo.entity.Item;
import com.spring_mongo.Spring_Mongo.service.ItemService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
public class ItemController {

    @Autowired
    private ItemService service;

    @GetMapping
    public List<Item> getAllItems() {
    	//System.out.println("hello");
        return service.getAllItems();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Item> getItemById(@PathVariable String id) {
        Optional<Item> item = service.getItemById(id);
        return item.map(ResponseEntity::ok)
                   .orElseGet(() -> ResponseEntity.notFound().build());
    }

    @PostMapping
    public Item createItem(@RequestBody Item item) {
        return service.saveItem(item);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Item> updateItem(@PathVariable String id, @RequestBody Item newItem) {
        return service.getItemById(id).map(existingItem -> {
            existingItem.setName(newItem.getName());
            existingItem.setDescription(newItem.getDescription());
            existingItem.setPrice(newItem.getPrice());
            return ResponseEntity.ok(service.saveItem(existingItem));
        }).orElseGet(() -> ResponseEntity.notFound().build());
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteItem(@PathVariable String id) {
        service.deleteItemById(id);
        return ResponseEntity.noContent().build();
    }
}