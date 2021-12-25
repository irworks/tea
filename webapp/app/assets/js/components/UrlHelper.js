export class UrlHelper {
    static setParameter(parameter, value) {
        const queryParams = new URLSearchParams(window.location.search);
        queryParams.set(parameter, value);
        history.replaceState(null, null, '?' + queryParams.toString());
    }

    static getParameter(parameter, fallback) {
        let value = new URL(window.location.href).searchParams.get(parameter);
        if (value) {
            return value;
        }

        return fallback;
    }
}