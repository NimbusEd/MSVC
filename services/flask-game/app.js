document.addEventListener('DOMContentLoaded', function () {
    // Fetch player data when the page loads
    fetchPlayerData();
});

function fetchPlayerData() {
    // Replace with the actual player ID
    const playerId = 1;

    // Fetch player data from the API
    fetch(`/api/player/${playerId}`)
        .then(response => response.json())
        .then(player => {
            // Update the UI with player information
            document.getElementById('username').textContent = player.username;
            document.getElementById('resources').textContent = player.resources;

            // Update the UI with building information
            const buildingList = document.getElementById('building-list');
            buildingList.innerHTML = ''; // Clear existing list

            player.buildings.forEach(building => {
                const listItem = document.createElement('li');
                listItem.textContent = `${building.name} (Level ${building.level})`;
                buildingList.appendChild(listItem);
            });
        })
        .catch(error => console.error('Error fetching player data:', error));
}

function upgradeBuilding() {
    // Replace with the actual player ID and building ID
    const playerId = 1;
    const buildingId = 1;

    // Send a request to upgrade the building
    fetch(`/api/player/${playerId}/upgrade-building`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ building_id: buildingId }),
    })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            // Update the UI after upgrading the building
            fetchPlayerData();
        })
        .catch(error => console.error('Error upgrading building:', error));
}
