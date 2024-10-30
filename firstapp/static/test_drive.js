document.getElementById('testDriveForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;
    const date = document.getElementById('date').value;
    const carModel = document.getElementById('carModel').value;
    
    // Here you would typically send this data to a server
    // For now, we'll just log it to the console
    console.log('Test Drive Booked:', { name, email, phone, date, carModel });
    
    alert('Test drive booked successfully!');
    this.reset();
});