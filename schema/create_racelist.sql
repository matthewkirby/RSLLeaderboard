-- Create the racelist table
CREATE TABLE IF NOT EXISTS racelist (
  slug TEXT PRIMARY KEY,    -- Unique identifier for the race
  url TEXT,                 -- URL of the race, racetime.gg/[url]
  ended_at DATETIME         -- Date and time when the race ended
);

-- Create the entrants table
CREATE TABLE IF NOT EXISTS entrants (
  id INTEGER PRIMARY KEY AUTOINCREMENT,   -- Unique identifier for each entrant
  race_slug TEXT,                         -- Foreign key referencing the racelist table
  user_id TEXT,                           -- User ID of the entrant
  status TEXT,                            -- Status of the entrant
  finish_time TEXT,                       -- Finish time of the entrant
  place INTEGER,                          -- Placement of the entrant
  comment TEXT,                           -- Comment associated with the entrant
  rating_before_mu REAL,                  -- Mu value for rating before the race
  rating_before_sigma REAL,               -- Sigma value for rating before the race
  rating_after_mu REAL,                   -- Mu value for rating after the race
  rating_after_sigma REAL,                -- Sigma value for rating after the race
  FOREIGN KEY (race_slug) REFERENCES racelist (slug)  -- Foreign key constraint
);