
insert into `mydb`.`University` ( `idUniversity`, `university_name`, `city`, `full_address`, `gps_coord1`, `gps_coord2`) 
values (1, 'ИТМО','Санкт-Петербург','197101, г. Санкт-Петербург, Кронверкский проспект, д.49.', 11.11,22.22);

insert into `mydb`.`Contacts` (
  `idContacts`,
  `phone_number`,
  `email` ) values (1, '+7(812)457-18-56', ' pyrkin@corp.ifmo.ru');

insert into `mydb`.`Contacts` (
  `idContacts`,
  `phone_number`,
  `email` ) values (2, '+7 (812) 457-18-56', 'mvnikitina@corp.ifmo.ru');

insert into `mydb`.`Faculty` (
  `idFaculty`,
  `idUniversity`,
  `faculty_name`,
  `descript`,
  `dean`,
  `num_of_foreign_students`,
  `website`,
  `address`,
  `Con_idContacts`)
  values (1, 1, 'Факультет систем управления и робототехники (ФСУиР)',
  ' ', ' ', 0, 'https://www.ifmo.ru/ru/viewfaculty/103/fakultet_sistem_upravleniya_i_robototehniki.htm',
  '197101, г. Санкт-Петербург, Кронверкский проспект, д.49.', 1 );



--- внесение учебных программ
insert into `mydb`.`Programme` (
  `idProgramme`,
  `programme_name`,
  `field_name`,
  `descript`,
  `education_level`,
  `language_of_study`,
  `fee_per_year`,
  `form_of_education`,
  `studies_duration`,
  `no_pay_positions`,
  `pay_positions`,
  `any_partner_univers`,
  `programme_director`,
  `person_to_contact`,
  `Con_idContacts`,
  `Dep_department_name`,
  `idUniversity`,
  `idFaculty`,
  `docs_url`,
  `docs_start_date`,
  `docs_end_date`) values (
  1, 'Информатика и вычислительная техника', '09.03.01', ' ',
  'Бакалавриат', 'Русский', 150000, 'Очная', 4, 10, 10, 1,
  'Никитина Мария Владимировна',  'Никитина Мария Владимировна', 2, ' ', 1,
  1, 'https://abit.ifmo.ru/bachelor/' ,  '2019-06-01', '2019-07-05' );

insert into `mydb`.`Contacts` (
  `idContacts`,
  `phone_number`,
  `email` ) values (3, '+7 (812) 457-18-56', 'ivanov@corp.ifmo.ru');

insert into `mydb`.`Programme` (
  `idProgramme`,
  `programme_name`,
  `field_name`,
  `descript`,
  `education_level`,
  `language_of_study`,
  `fee_per_year`,
  `form_of_education`,
  `studies_duration`,
  `no_pay_positions`,
  `pay_positions`,
  `any_partner_univers`,
  `programme_director`,
  `person_to_contact`,
  `Con_idContacts`,
  `Dep_department_name`,
  `idUniversity`,
  `idFaculty`,
  `docs_url`,
  `docs_start_date`,
  `docs_end_date`) values (
  2, 'Технология приборостроения', '12.03.01', ' ',
  'Бакалавриат', 'Русский', 100000, 'Очная', 4, 10, 5, 1,
  'Иванов Иван Иванович',  'Иванов Иван Иванович', 3, ' ', 1,
  1, 'https://abit.ifmo.ru/bachelor/',   '2019-06-01', '2019-07-01' );


 --- необходимые ЕГЭ

--- заполнение справочиков ЕГЭ
insert into `mydb`.`ege_dictionary` (`egeid`, `ege_name`)
values (1, 'Математика');
insert into `mydb`.`ege_dictionary` (`egeid`, `ege_name`)
values (2, 'Физика');
insert into `mydb`.`ege_dictionary` (`egeid`, `ege_name`)
values (3, 'Информатика');

insert into `mydb`.`ege_requirements` (
  `egeid`,
  `min_value`,
  `idUniversity`,
  `idProgramme`) values (
    1, 70, 1, 1 );

insert into `mydb`.`ege_requirements` (
  `egeid`,
  `min_value`,
  `idUniversity`,
  `idProgramme`) values (
    2, 60, 1, 1 );

insert into `mydb`.`ege_requirements` (
  `egeid`,
  `min_value`,
  `idUniversity`,
  `idProgramme`) values (
    3, 60, 1, 1 );

insert into `mydb`.`non_ege_exams_dictionary` (
  `idNonEgeExam`,
  `exam_name`,
  `max_value`) values (1, 'Физика', 5);

insert into `mydb`.`non_ege_exams_dictionary` (
  `idNonEgeExam`,
  `exam_name`,
  `max_value`) values (2, 'Математика', 5);

insert into  `mydb`.`Programme_non_ege_ExamRequired` (
  `idProgramme`,
  `idNonEgeExam`,
  `min_value`,
  `exam_date`) values (1, 1, 3, '03.07.2019');

insert into  `mydb`.`Programme_non_ege_ExamRequired` (
  `idProgramme`,
  `idNonEgeExam`,
  `min_value`,
  `exam_date`) values (1, 2, 3, '09.08.2019');

