package com.springboot.mysql.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.springboot.mysql.entity.User;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
}
