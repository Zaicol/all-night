async function ready() {
  document.getElementById('submit').value = 'Сохранить';
  const { pid } = document.getElementById('editform').dataset
  console.log(pid);
  const response = await fetch(
    (`/api/pid` + pid)
  );
  if(response != null){
    const data = (await response.json())[0];
    console.log(data);
    document.getElementById('title').value = data['title'];
    document.getElementById('content').value = data['content'];
    document.getElementById('dt').value = data['dt'];
    document.getElementById('lat').value = data['lat'];
    document.getElementById('lon').value = data['lon'];
  }
  return false;
}

document.addEventListener("DOMContentLoaded", ready);