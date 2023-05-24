const bytesToSize = (bytes) => {
    const sizes = ["Bytes", "KB", "MB", "GB", "TB"];  
    if (bytes === 0) {
      return "0 Byte";
    }
    const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));  
    return Math.round(bytes / Math.pow(1024, i), 2) + " " + sizes[i];
}

const compressImage = async (file, { quality = 1, type = file.type }) => {
    // Get as image data
    const imageBitmap = await createImageBitmap(file);

    // Draw to canvas
    const canvas = document.createElement('canvas');
    canvas.width = imageBitmap.width;
    canvas.height = imageBitmap.height;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(imageBitmap, 0, 0);

    // Turn into Blob
    const blob = await new Promise((resolve) =>
        canvas.toBlob(resolve, type, quality)
    );

    if (blob) {
        let compressedImageBlob = blob;
        const ele = document.querySelector('#img-preview');
        ele.style.display = 'block';
        ele.src = URL.createObjectURL(compressedImageBlob);
        ele.width = 200;
        ele.height = 200;
        console.log(bytesToSize(blob.size));
    }

    // Turn Blob into File
    return new File([blob], file.name, {
        type: blob.type,
    });
};


let compress = async (e) =>{

    console.log('compressing..')
    
    // Get the files
    const { files } = e.target;

    // No files selected
    if (!files.length) return;

    // We'll store the files in this data transfer object
    const dataTransfer = new DataTransfer();

    // For every file in the files list
    for (const file of files) {
        // We don't have to compress files that aren't images
        if (!file.type.startsWith('image')) {
            // Ignore this file, but do add it to our result
            dataTransfer.items.add(file);
            continue;
        }

        // We compress the file by 50%
        const compressedFile = await compressImage(file, {
            quality: 0.5,
            type: 'image/jpeg',
        });

        // Save back the compressed file instead of the original file
        dataTransfer.items.add(compressedFile);
    }

    // Set value of the file input to our new files list
    e.target.files = dataTransfer.files;
}