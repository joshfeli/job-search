BEGIN TRY
    CREATE DATABASE jobs; /* create the database once */
END TRY
BEGIN CATCH
    SELECT NULL /* do nothing */
END CATCH
