package com.springboot.mysql.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.springboot.mysql.entity.MediaFile;

@Repository
public interface MediaFileRepository extends JpaRepository<MediaFile,Long>{

}
