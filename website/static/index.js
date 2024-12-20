function deleteWrapped(wrappedId) {
    fetch("/delete-wrapped", {
        method: "POST",
        body: JSON.stringify({ wrappedId: wrappedId }),
    }).then((_res) => {
        window.location.href = "/";
    });
}