import axios from 'axios';

import * as settings from './conf';

// TODO: users API endpoints

// ------------ START: catalog API endpoints ------------

/**
 * Fetch categories from catalog API endpoint.
 */
export const fetchCatalogCategories = async function (params = {}) {
    const response = await axios.get(`${settings.API_ROOT}catalog/categories`, {
        params: { ...params },
    });
    const categories = response?.data?.results || [];
    return categories;
};

/**
 * Fetch layers from catalog API endpoint.
 */
export const fetchCatalogLayers = async function (params = {}) {
    const response = await axios.get(`${settings.API_ROOT}catalog/layers`, {
        params: { ...params },
    });
    const layers = response?.data?.results || [];
    return layers;
};

// ------------ END: catalog API endpoints ------------

// ------------ START: administrative API endpoints ------------

/**
 * Fetch countries from administrative areas API endpoint.
 */
export const fetchCountries = async function (params = {}) {
    const response = await axios.get(`${settings.API_ROOT}administrative/areas`, {
        params: { level: 1, exclude_geometry: 1, ...params },
    });
    const countries = response.data;
    return countries;
};

/**
 * Fetch regions from administrative areas API endpoint.
 */
export const fetchRegions = async function (params = {}) {
    const response = await axios.get(`${settings.API_ROOT}administrative/areas`, {
        params: { level: 2, exclude_geometry: 1, ...params },
    });
    const regions = response.data;
    return regions;
};

// ------------ END: administrative API endpoints ----------

// TODO: demographics API endpoints
// TODO: education API endpoints
// TODO: infrastructure API endpoints
