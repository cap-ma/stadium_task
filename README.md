# Football Field Booking System

This project is a Django REST Framework-based API for managing football (stadium) bookings. It includes endpoints for creating and managing football fields, images, and bookings. The API supports filtering available fields based on booking time and user location, with performance optimizations like pagination and indexing.

## Features

- **User Roles:**  
  - **Admin**: Full control over the system.  
  - **Stadium Owner**: Manage their own football fields and view/delete bookings.  
  - **Client**: View available fields and make bookings.
  
- **Football Field Management:**  
  - Create, update, delete, and list football fields.
  - Each field can have multiple images.
  
- **Booking System:**  
  - Clients can book a football field.
  - Conflict detection ensures a field isn't double-booked for overlapping times.
  
- **Filtering and Sorting:**  
  - Filter available fields by booking date, start time, and end time.
  - Sort fields based on proximity using the user's latitude and longitude.
  
- **API Documentation:**  
  - Swagger UI (using drf_yasg) for interactive API docs.
  
- **Performance Optimizations:**  
  - **Pagination:** Only fetches a limited number of records per page, dramatically reducing response times.
  I tried 2000 objects per page and it took 2.0 secunds
  - **Database Indexing:** Indexes on frequently queried fields to speed up database lookups.
  after indexing it went down around 1.4 secunds for 2000  objects
  - **Database-level Calculations:** Distance calculations are done at the database level (when using a proper backend) to reduce Python-level processing. (it did not help to decrease query time even if i wrapped computation logic of distance and exucute it in database level )

   **Further Optimization:**
   Further optimization and real-life like scenaria may be implemented by using PostGis and some other technologies but for this test task i wanted it to be easy and understandable


