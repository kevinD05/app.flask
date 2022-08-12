instrucions = [
    'SET FOREIGN_KEY_CHECKS=0;',
    'DROP TABLE IF EXISTS todo;',
    'DROP TABLE IF EXISTS user;',
    'SET FOREIGN_KEY_CHECKS=1;',

    """
        CREATE TABLE user(
            id INT PRIMARY KEY AUTO_INCREMENT,
            idk VARCHAR(10) NOT NULL,
            username varchar(50) UNIQUE NOT NULL,
            password varchar(100) NOT NULL
        )
    """,
    """
        CREATE TABLE todo(
            id INT PRIMARY KEY AUTO_INCREMENT,
            created_by INT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            descriptcion TEXT NOT NULL,
            completed BOOLEAN NOT NULL,
            FOREIGN KEY (created_by) REFERENCES user (id)
        );
    """
]