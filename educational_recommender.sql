USE educational_recommender;
CREATE TABLE USERS (
  id             CHAR(36)      NOT NULL DEFAULT (UUID()),
  full_name      VARCHAR(100)  NOT NULL,
  email          VARCHAR(150)  NOT NULL UNIQUE,
  password_hash  VARCHAR(255)  NOT NULL,
  specialization VARCHAR(100),
  level          ENUM('beginner','intermediate','advanced'),
  created_at     TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
  last_login     TIMESTAMP,
  PRIMARY KEY (id)
);

CREATE TABLE CONTENT (
  id         CHAR(36)     NOT NULL DEFAULT (UUID()),
  title      VARCHAR(255) NOT NULL,
  type       ENUM('article','course','video') NOT NULL,
  url        TEXT         NOT NULL,
  field      VARCHAR(100),
  level      ENUM('beginner','intermediate','advanced'),
  avg_rating FLOAT        DEFAULT 0,
  created_at TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
);

CREATE TABLE TAGS (
  id   CHAR(36)    NOT NULL DEFAULT (UUID()),
  name VARCHAR(80) NOT NULL UNIQUE,
  PRIMARY KEY (id)
);

CREATE TABLE CONTENT_TAGS (
  content_id CHAR(36) NOT NULL,
  tag_id     CHAR(36) NOT NULL,
  PRIMARY KEY (content_id, tag_id),
  FOREIGN KEY (content_id) REFERENCES CONTENT(id) ON DELETE CASCADE,
  FOREIGN KEY (tag_id)     REFERENCES TAGS(id)    ON DELETE CASCADE
);

CREATE TABLE INTERACTIONS (
  id               CHAR(36)  NOT NULL DEFAULT (UUID()),
  user_id          CHAR(36)  NOT NULL,
  content_id       CHAR(36)  NOT NULL,
  action           ENUM('viewed','liked','rated','bookmarked') NOT NULL,
  rating           FLOAT,
  duration_seconds INT       DEFAULT 0,
  interacted_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  FOREIGN KEY (user_id)    REFERENCES USERS(id)   ON DELETE CASCADE,
  FOREIGN KEY (content_id) REFERENCES CONTENT(id) ON DELETE CASCADE
);

CREATE TABLE RECOMMENDATIONS (
  id           CHAR(36)    NOT NULL DEFAULT (UUID()),
  user_id      CHAR(36)    NOT NULL,
  content_id   CHAR(36)    NOT NULL,
  score        FLOAT       NOT NULL,
  algorithm    VARCHAR(60) NOT NULL,
  clicked      BOOLEAN     DEFAULT FALSE,
  generated_at TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  FOREIGN KEY (user_id)    REFERENCES USERS(id)   ON DELETE CASCADE,
  FOREIGN KEY (content_id) REFERENCES CONTENT(id) ON DELETE CASCADE
);

CREATE TABLE SESSIONS (
  id         CHAR(36)  NOT NULL DEFAULT (UUID()),
  user_id    CHAR(36)  NOT NULL,
  token      TEXT      NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  FOREIGN KEY (user_id) REFERENCES USERS(id) ON DELETE CASCADE
);