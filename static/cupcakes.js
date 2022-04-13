BASE_URL = 'http://127.0.0.1:5000/'

// ** Get all cupcakes and show on page load **
$(getAndShowCupcakes())

const $cupcakeForm = $('.add-cupcake-form')

// ** Get and show cupcakes when site first loads **
async function getAndShowCupcakes() {
    const res = await axios({
        url: `${BASE_URL}/api/cupcakes`,
        method: "GET"
    })

    const cupcakes = res.data.cupcakes;
    console.log(cupcakes);
    showCupcakesList(cupcakes, cupcakes.length)
}

// ** Render HTML for cupcakes and append to DOM **
async function showCupcakesList(cupcakes, count) {
    for(let i = 0; i < count; i++) {
        $('#cupcakes-list').append(GenerateCupcakeMarkup(cupcakes[i]));
    }
}

// ** Render and return HTML for a cupcake instance **
function GenerateCupcakeMarkup(cupcake) {
    const HTMLCupcake = $(`<figure class="figure col-md-3 col-sm-auto" id=${cupcake.id}>
        <img src="${cupcake.image}" alt="cupcake" class="img-thumbnail">
        <figcaption>
            <ul data=${cupcake.id}>
                <li>Flavor: ${cupcake.flavor}</li>
                <li>Size: ${cupcake.size}</li>
                <li>Rating: ${cupcake.rating}</li>
                <li data-id=${cupcake.id} class="btn btn-outline-danger btn-small">
                    Delete
                </li>
            </ul>
        </figcaption>
      </figure>`
    )
    return HTMLCupcake;
}

// ** Triggers add cupcake handle when form is submitted
$('#add-cupcake-form').on('submit', addCupcake)

// ** Handle form submission for adding cupcake
async function addCupcake(evt) {
    evt.preventDefault();
    console.log("on submit");

    const res = await axios({
        url: `${BASE_URL}/api/cupcakes`,
        method: 'POST',
        data: {
            'flavor': `${$('#flavor').val()}`,
            'size': `${$('#size').val()}`,
            'rating': `${$('#rating').val()}`,
            'image': `${$('#image-url').val()}`
        }
    })
    $('#cupcakes-list').prepend(GenerateCupcakeMarkup(res.data.cupcake));
    $('#add-cupcake-form').trigger('reset');
}

// ** Handle clicking delete 
$('#cupcakes-list').on('click', delete_cupcake)

// ** delete cupcake
async function delete_cupcake(evt) {
    evt.preventDefault();

    if(evt.target.className == 'btn btn-outline-danger btn-small') {

        id = evt.target.dataset.id;
        res = await axios({
            url: `${BASE_URL}/api/cupcakes/${id}`,
            method: 'DELETE'
        })
        console.log(res.data)
        $(`#${id}`).remove();
    }
}