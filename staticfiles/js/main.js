    let tags = document.getElementsByClassName('project-tag')
    for(let i = 0; tags.length >i; i++){
        tags[i].addEventListener('click', (e)=> {
            let tagId = e.target.dataset.tag
            let playerId = e.target.dataset.player

            fetch('http://127.0.0.1:8000/api/remove-tag/', {
                method: 'DELETE',
                headers:{
                'Content-Type': 'application/json'
                },
                body: JSON.stringify({'player': playerId, 'tag': tagId})
            })
                .then(response => response.json())
                .then(data =>{
                    e.target.remove()
                })
        })
    }