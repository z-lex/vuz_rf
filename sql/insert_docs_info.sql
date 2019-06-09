insert into `mydb`.`documet_dictionary` (
  `idDoc`,
  `doc_name`,
  `is_common_doc`) values (
  1, 'Аттестат или диплом о среднем специальном образовании',
  1);


insert into `mydb`.`documet_dictionary` (
  `idDoc`,
  `doc_name`,
  `is_common_doc`) values (
  2, 'Паспорт РФ',
  1);


insert into `mydb`.`documet_dictionary` (
  `idDoc`,
  `doc_name`,
  `is_common_doc`) values (
  3, 'Справка 086у',
  1);


insert into `mydb`.`documet_dictionary` (
  `idDoc`,
  `doc_name`,
  `is_common_doc`) values (
  4, 'Прививочный сертификат',
  1);


insert into `mydb`.`documet_dictionary` (
  `idDoc`,
  `doc_name`,
  `is_common_doc`) values (
  5, 'Полис ОМС',
  1);
  
  insert into `mydb`.`documet_dictionary` (
  `idDoc`,
  `doc_name`,
  `is_common_doc`) values (
  6, 'Фото',
  1);

 -- для ИВТ
insert into `mydb`.`docs_required` (
  `key`,
  `idProgramme`,
  `idDoc`) values (0, 1, 1);

insert into `mydb`.`docs_required` (
  `key`,
  `idProgramme`,
  `idDoc`) values (0, 1, 2);

insert into `mydb`.`docs_required` (
  `key`,
  `idProgramme`,
  `idDoc`) values (0, 1, 3);

insert into `mydb`.`docs_required` (
  `key`,
  `idProgramme`,
  `idDoc`) values (0, 1, 4);

insert into `mydb`.`docs_required` (
  `key`,
  `idProgramme`,
  `idDoc`) values (0, 1, 5);

-- для приборостроения
insert into `mydb`.`docs_required` (
  `key`,
  `idProgramme`,
  `idDoc`) values (0, 2, 1);

insert into `mydb`.`docs_required` (
  `key`,
  `idProgramme`,
  `idDoc`) values (0, 2, 2);

insert into `mydb`.`docs_required` (
  `key`,
  `idProgramme`,
  `idDoc`) values (0, 2, 3);

insert into `mydb`.`docs_required` (
  `key`,
  `idProgramme`,
  `idDoc`) values (0, 2, 4);

insert into `mydb`.`docs_required` (
  `key`,
  `idProgramme`,
  `idDoc`) values (0, 2, 5);

-- для приборостроения
insert into `mydb`.`docs_required` (
  `key`,
  `idProgramme`,
  `idDoc`) values (0, 4, 1);

insert into `mydb`.`docs_required` (
  `key`,
  `idProgramme`,
  `idDoc`) values (0, 4, 2);

insert into `mydb`.`docs_required` (
  `key`,
  `idProgramme`,
  `idDoc`) values (0, 4, 3);

insert into `mydb`.`docs_required` (
  `key`,
  `idProgramme`,
  `idDoc`) values (0, 4, 4);

insert into `mydb`.`docs_required` (
  `key`,
  `idProgramme`,
  `idDoc`) values (0, 4, 5);