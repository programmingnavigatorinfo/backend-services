package com.spring_mongo.Spring_Mongo.entity;

import org.bson.types.Binary;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;
import org.springframework.data.mongodb.core.mapping.MongoId;

import lombok.Data;

@Data
@Document(collection="media_files")
public class MediaFile {
	
	@MongoId
	@Field("file_id")
	private String id;
	
	
	@Field("file_name")
	private String title;
	
	@Field("file_size")
	private long size;
	
	@Field("file_type")
	private String fileType;
	
	@Field("file_data")
	private Binary fileData;

	public String getId() {
		return id;
	}

	public void setId(String id) {
		this.id = id;
	}

	public String getTitle() {
		return title;
	}

	public void setTitle(String title) {
		this.title = title;
	}

	public long getSize() {
		return size;
	}

	public void setSize(long size) {
		this.size = size;
	}

	public String getFileType() {
		return fileType;
	}

	public void setFileType(String fileType) {
		this.fileType = fileType;
	}

	public Binary getFileData() {
		return fileData;
	}

	public void setFileData(Binary fileData) {
		this.fileData = fileData;
	}

	public MediaFile(String id, String title, long size, String fileType, Binary fileData) {
		super();
		this.id = id;
		this.title = title;
		this.size = size;
		this.fileType = fileType;
		this.fileData = fileData;
	}
	
	public MediaFile() {}
	

}
