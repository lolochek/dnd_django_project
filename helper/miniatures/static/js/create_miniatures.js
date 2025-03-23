 const { jsPDF } = window.jspdf;

 const gridConfig = {
    small: { rows: 7, height: 1, width: 1.5 },
    medium: { rows: 5, height: 1.5, width: 2.5 },
    large: { rows: 3, height: 2, width: 4 },
    giant: { rows: 2, height: 2.5, width: 4 }
};

     function updateGrid() {
        const size = document.getElementById('sizeSelect').value;
        const { rows, height, width } = gridConfig[size];
        const gridContainer = document.getElementById('gridContainer');
        const topCirclesContainer = document.getElementById('topCirclesContainer');
        gridContainer.innerHTML = '';
        topCirclesContainer.innerHTML = '';

        for (let i = 0; i < rows; i++) {
            let row = document.createElement('div');
            row.classList.add('d-flex', 'align-items-center', 'justify-content-center', 'mb-2');
            row.style.position = 'relative';

            let leftSemiCircle = document.createElement('div');
            leftSemiCircle.style.width = `${height * 0.5}in`;
            leftSemiCircle.style.height = `${height}in`;
            leftSemiCircle.classList.add('side-semi-circle', 'left');
            let rightSemiCircle = document.createElement('div');
            rightSemiCircle.style.width = `${height * 0.5}in`;
            rightSemiCircle.style.height = `${height}in`;
            rightSemiCircle.classList.add('side-semi-circle', 'right');

            let col1 = document.createElement('div');
            col1.classList.add('image-cell');
            col1.style.width = `${width}in`;
            col1.style.height = `${height}in`;
            let col2 = col1.cloneNode();

            row.appendChild(leftSemiCircle);
            row.appendChild(col1);
            row.appendChild(col2);
            row.appendChild(rightSemiCircle);

            gridContainer.appendChild(row);


        }

       for (let i = 0; i < rows; i++) {
            let circle = document.createElement('div');
            circle.classList.add('circle');
            circle.style.width = `${height}in`;
            circle.style.height = `${height}in`;
            topCirclesContainer.appendChild(circle);
        }

        updateSideColors();
        addImagesToCells();
    }

    function updateSideColors() {
        const color = document.getElementById('colorPicker').value;
        document.querySelectorAll('.side-semi-circle, .circle').forEach(circle => {
            circle.style.backgroundColor = color;
        });
    }

   function addImagesToCells() {
    const cells = document.querySelectorAll('.image-cell');
    const files = document.getElementById('imageUpload').files;
    if (!files.length) return;

    let fileIndex = 0;
    cells.forEach((cell, index) => {
        const reader = new FileReader();
        reader.onload = function(e) {
            const img = document.createElement('img');
            img.src = e.target.result;
            img.style.width = '80%';
            img.style.height = 'auto';
            img.style.objectFit = 'cover';
            img.style.objectPosition = 'center';
            cell.innerHTML = '';
            cell.appendChild(img);

            if (index % 2 === 0) {
                img.classList.add('rotate-right');
            } else {
                img.classList.add('rotate-left');
            }
        };
        reader.readAsDataURL(files[fileIndex]);
        fileIndex = (fileIndex + 1) % files.length;
    });
}


    function exportToPDF() {
        const canvasContainer = document.getElementById('canvasContainer');

        html2canvas(canvasContainer, {
            scale: 2,
            useCORS: true
        }).then(canvas => {
            const pdf = new jsPDF({
                orientation: 'portrait',
                unit: 'mm',
                format: 'a4'
            });

            const imgData = canvas.toDataURL('image/png');
            const imgWidth = 210;
            const imgHeight = (canvas.height * imgWidth) / canvas.width;

            pdf.addImage(imgData, 'PNG', 0, 0, imgWidth, imgHeight);
            pdf.save("miniatures.pdf");
        }).catch(err => {
            console.error("Ошибка при создании PDF:", err);
        });
    }

    updateGrid();