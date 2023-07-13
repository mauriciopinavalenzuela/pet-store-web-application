let url='https://api.thedogapi.com/v1/breeds?limit=10&page=0';
fetch(url)
	.then(response =>response.json())
	.then(data => mostrarData(data))
	.catch(error => console.log(error))

const mostrarData=(data)=>{
	console.log(data)
	let body=""
	for (var i=0; i<data.length; i++)
	{
		body+=`<tr>                      
			<td>${data[i].id}</td>       
			<td>${data[i].name}</td>
			<td>${data[i].temperament}</td>
			<td>${data[i].origin}</td>
			<td>${data[i].life_span}</td>
			<td><img src="${data[i].image.url}" alt="${data[i].name}"></td>
			</tr>`
	}
	document.getElementById('data').innerHTML=body
}
