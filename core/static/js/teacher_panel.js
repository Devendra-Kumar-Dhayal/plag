function toggleContent(section) {
    var groupsContent = document.getElementById('groups-content');
    var filesContent = document.getElementById('files-content');
    var uploadedFilesContainer = document.getElementById('uploaded-files-container');
    var groupsLink = document.querySelector('.sidebar-menu a[onclick="toggleContent(\'groups\')"]');
    var filesLink = document.querySelector('.sidebar-menu a[onclick="toggleContent(\'files\')"]');

    if (section === 'files' ) {
        groupsContent.style.display = 'none';
        filesContent.style.display = 'block';
        uploadedFilesContainer.style.display = 'block';
        
        groupsLink.classList.remove('active');
        filesLink.classList.add('active');
        
        
    } else if (section === 'groups') {
        groupsContent.style.display = 'block';
        filesContent.style.display = 'none';
        uploadedFilesContainer.style.display = 'none';
        groupsLink.classList.add('active');
        filesLink.classList.remove('active');
        
    }
}