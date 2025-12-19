const classrooms = [
  { id: '1', grade: 1, section: 'A' },
  { id: '2', grade: 2, section: 'B' }
];

const students = [
  { id: '1', firstName: 'Ana', lastName: 'García', email: 'ana@example.com', classroomId: '1' }
];

function findClassroom(id) {
  return classrooms.find((classroom) => classroom.id === id);
}

function findStudent(id) {
  return students.find((student) => student.id === id);
}

function nextId(collection) {
  return (collection.length + 1).toString();
}

module.exports = {
  classrooms,
  students,
  findClassroom,
  findStudent,
  nextId
};
