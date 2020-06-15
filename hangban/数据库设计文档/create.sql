# 创建航班表格
drop table if exists hangban_pek;
CREATE TABLE hangban_pek (
    id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    date DATE NOT NULL,
    agent VARCHAR(30),
    company VARCHAR(30),
    Flight_nb VARCHAR(30) NOT NULL,
    Machine_nb VARCHAR(30),
    Model VARCHAR(30),
    Model_Cate VARCHAR(30),
    terminal VARCHAR(30),
    Domestic_Inter VARCHAR(30),
    Planned_arrival DATETIME,
    Planned_depart DATETIME,
    Actual_arrival DATETIME,
    Actual_depart DATETIME,
    First_TSAT DATETIME,
    Last_TSAT DATETIME,
    First_RDY_time DATETIME,
    RDY_time DATETIME,
    ASAT DATETIME,
    Actual_take_off DATETIME,
    former_actual_landing DATETIME,
    Plan_Station INT,
    Seat VARCHAR(30),
    Apron VARCHAR(30),
    Near_and_far VARCHAR(30),
    Task_Nature VARCHAR(30),
    Runway VARCHAR(30),
    Cancel_Status VARCHAR(30),
    Boarding_start DATETIME,
    Boarding_end DATETIME,
    Opening_cabin_door DATETIME,
    Opening_cargo_Door DATETIME,
    Closing_cabin_door DATETIME,
    Closing_cargo_door DATETIME,
    Entry_braking_time DATETIME,
    Loosen_braking_departure DATETIME,
    Bridge_start_elevator DATETIME,
    Bridge_removal_elevator DATETIME,
    First_ferry_gate DATETIME,
    Final_ferry_gate DATETIME,
    Trailer_in_place DATETIME,
    Incoming_elevator_logo VARCHAR(30),
    Take_off_Delay VARCHAR(30),
    Inter_and_exter VARCHAR(30),
    Early_depar_Initial VARCHAR(30),
    Min_crossing_Station INT,
    STA DATETIME,
    ATA DATETIME,
    Need_use_Ferry VARCHAR(30),
    Incoming_elevator_inplace DATETIME,
    Incoming_First_arrival DATETIME,
    Incoming_First_logo VARCHAR(30),
    Passengers_Number INT UNSIGNED,
    In_Out_Sign VARCHAR(30) NOT NULL,
    ETA DATETIME,
    Transit_delay VARCHAR(30),
    Departure_delay VARCHAR(30),
    UNIQUE INDEX (In_Out_Sign , Flight_nb , date)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


# 如果需要，可考虑构建如下索引
CREATE INDEX INDEX index_com ON hangban_pek (In_Out_Sign , Cancel_Status , company , date);
CREATE INDEX INDEX index_off ON hangban_pek (In_Out_Sign , company , Cancel_Status , Take_off_Delay , date);
CREATE INDEX INDEX index_ferry ON hangban_pek (In_Out_Sign , Cancel_Status , agent , Need_use_Ferry , date);
CREATE INDEX INDEX index_elevator ON hangban_pek (In_Out_Sign , agent , Incoming_elevator_logo , date);
CREATE INDEX INDEX index_early ON hangban_pek (In_Out_Sign , Cancel_Status , company , Early_depar_Initial , date);
CREATE INDEX INDEX index_flight ON hangban_pek (In_Out_Sign , Cancel_Status , Flight_nb , Take_off_Delay , date);


# 创建机场信息表
drop table if exists airport_info;
create TABLE airport_info (
  id INT NOT NULL AUTO_INCREMENT,
  IATA VARCHAR(5) NOT NULL,
  ICAO VARCHAR(5) NOT NULL,
  airport_eng VARCHAR(45) NULL,
  airport_chi VARCHAR(45) NULL,
  guan VARCHAR(45) NULL,
  province VARCHAR(45) NULL,
  country_id VARCHAR(5) NULL,
  country_chi VARCHAR(45) NULL,
  airport_style VARCHAR(10) NULL,
  city VARCHAR(45) NULL,
  PRIMARY KEY (id),
  UNIQUE INDEX id_UNIQUE (id ASC) VISIBLE,
  UNIQUE INDEX IATA_UNIQUE (IATA ASC) VISIBLE
)ENGINE=InnoDB DEFAULT CHARSET=utf8;



# 创建航空公司信息表
drop table if exists airline_info;
create TABLE airline_info (
  id INT NOT NULL AUTO_INCREMENT,
  IATA VARCHAR(5) NOT NULL,
  ICAO VARCHAR(5) NOT NULL,
  airline_eng VARCHAR(45) NULL,
  airline_chi VARCHAR(45) NULL,
  airline_airport VARCHAR(5) NULL,
  chi_simple VARCHAR(45) NULL,
  airline_style VARCHAR(5) NULL,
  country VARCHAR(5) NULL,
  logo VARCHAR(5) NULL,
  guan VARCHAR(45) NULL,
  PRIMARY KEY (id),
  UNIQUE INDEX id_UNIQUE (id ASC) VISIBLE,
  UNIQUE INDEX IATA_UNIQUE (IATA ASC) VISIBLE
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
