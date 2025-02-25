export const updateURLParams = (url, params) => {
    const _url = new URL(url);
    for (const key in params) {
        _url.searchParams.set(key, params[key]);
    }
    return _url;
};
