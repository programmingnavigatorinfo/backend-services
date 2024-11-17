package com.mydbconnect.MysqlConnect;


import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class DatabaseConnectionChecker implements CommandLineRunner {

    @Value("${spring.datasource.url}")        // Injecting URL from application.properties
    private String dbUrl;

    @Value("${spring.datasource.username}")   // Injecting username from application.properties
    private String dbUsername;

    @Value("${spring.datasource.password}")   // Injecting password from application.properties
    private String dbPassword;

    @Override
    public void run(String... args) throws Exception {
        try (Connection connection = DriverManager.getConnection(dbUrl, dbUsername, dbPassword)) {
            // Test the connection
            if (connection != null) {
                System.out.println("MySQL Database Connected successfully!");
            }
        } catch (SQLException e) {
            System.err.println("MySQL Connection failed: " + e.getMessage());
        }
    }
}
