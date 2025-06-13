import maplibregl from 'maplibre-gl';


 /**
 * Create a popup for the education institutions layer features.
 *
 *
 * This:
 *
 * - Fetch `country` name based on clicked education institution
 * - Fetch `region` name based on clicked education institution
 * - Display a popup with education institution properties
 */
export const educationInstitutionPopup = async function (event, countries){
    const countryName = countries[event.features[0].properties.country];
    const name = `${event.features[0].properties.name}`;
    const selectedRegion = event.features[0].properties.administrative_area_name;

    if (this.currentPopup){
        this.currentPopup.remove();
    }

    popup = new maplibregl.Popup()
        .setLngLat(e.lngLat)
        .setHTML(
            `<div class="card border-0">
                <div class="card-header text-bg-primary">
                  <h5 class="text-white pe-3">${name}</h5>
                </div>

                <div class="card-body">
                    <p class="text-uppercase fs-6 fw-light text-muted">
                        Country : ${countryName}
                    </p>
                    <p class="text-uppercase fs-6 fw-light text-muted">
                        Region : ${selectedRegion}
                    </p>

                </div>
            </div>`,
        )
    return popup
}
