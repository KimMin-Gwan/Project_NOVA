import React, { useState } from 'react';

const ImageUploadWithJson = () => {
  const [image, setImage] = useState(null);
  const [jsonData, setJsonData] = useState({ title: '', description: '' });

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setImage(file);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setJsonData({ ...jsonData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!image) {
      console.error('No image selected');
      return;
    }

    const formData = new FormData();
    formData.append('image', image);
    formData.append('jsonData', JSON.stringify(jsonData)); // JSON을 문자열로 변환하여 전송

    try {
      const response = await fetch('http://127.0.0.1:4000/upload', {
        method: 'POST',
        body: formData,
      });
      if (response.ok) {
        console.log('Image and JSON data uploaded successfully');
      } else {
        console.error('Failed to upload');
      }
    } catch (error) {
      console.error('Error uploading:', error);
    }
  };

  return (
    <div>
      <h2>Upload Image with JSON Data</h2>
      <form onSubmit={handleSubmit}>
        <input type="file" accept="image/*" onChange={handleImageChange} />
        <input
          type="text"
          name="title"
          value={jsonData.title}
          onChange={handleInputChange}
          placeholder="Title"
        />
        <input
          type="text"
          name="description"
          value={jsonData.description}
          onChange={handleInputChange}
          placeholder="Description"
        />
        <button type="submit">Upload</button>
      </form>
    </div>
  );
};

export default ImageUploadWithJson;
