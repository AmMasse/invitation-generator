import sys
import pandas as pd
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os
from reportlab.lib.pagesizes import A5
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
import json

# Set appearance mode and color theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class InvitePDF:
    def __init__(self, template_settings, template_image_path=None):
        self.settings = template_settings
        self.template_image = template_image_path
        
    def create_invite(self, guest_name, link, occasion, filename):
        # A5 dimensions: 148x210mm
        width, height = A5
        
        # Create canvas
        c = canvas.Canvas(filename, pagesize=A5)
        
        # First, draw the background template if provided
        if self.template_image and os.path.exists(self.template_image):
            try:
                # Open and resize image to fit A5
                img = Image.open(self.template_image)
                
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # Resize to A5 dimensions while maintaining aspect ratio
                img_width, img_height = img.size
                target_width = int(width)
                target_height = int(height)
                
                # Calculate scaling to fit A5 exactly
                scale_w = target_width / img_width
                scale_h = target_height / img_height
                scale = max(scale_w, scale_h)  # Use max to fill the page
                
                new_width = int(img_width * scale)
                new_height = int(img_height * scale)
                
                # Resize image
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Center the image if it's larger than A5
                x_offset = (new_width - target_width) // 2
                y_offset = (new_height - target_height) // 2
                
                if x_offset > 0 or y_offset > 0:
                    img = img.crop((x_offset, y_offset, x_offset + target_width, y_offset + target_height))
                
                # Draw the background image
                c.drawImage(ImageReader(img), 0, 0, width=width, height=height)
                
            except Exception as e:
                print(f"Error loading template image: {e}")
                # Continue without background image
        
        # Define text zones based on template settings
        # These coordinates are defined as positions from bottom-left (ReportLab standard)
        
        # Guest Name Zone
        if self.settings['show_guest_name']:
            c.setFont("Helvetica-Bold", self.settings['name_font_size'])
            c.setFillColor(colors.Color(
                self.settings['name_color'][0]/255,
                self.settings['name_color'][1]/255,
                self.settings['name_color'][2]/255
            ))
            
            name_text = f"Dear {guest_name},"
            x_pos = self.settings['name_x'] * mm
            y_pos = self.settings['name_y'] * mm
            
            if self.settings['name_align'] == 'center':
                text_width = c.stringWidth(name_text, "Helvetica-Bold", self.settings['name_font_size'])
                x_pos = (width - text_width) / 2
            elif self.settings['name_align'] == 'right':
                text_width = c.stringWidth(name_text, "Helvetica-Bold", self.settings['name_font_size'])
                x_pos = width - text_width - (self.settings['name_x'] * mm)
                
            c.drawString(x_pos, y_pos, name_text)
        
        # Main Message Zone
        if self.settings['show_main_message']:
            c.setFont("Helvetica", self.settings['message_font_size'])
            c.setFillColor(colors.Color(
                self.settings['message_color'][0]/255,
                self.settings['message_color'][1]/255,
                self.settings['message_color'][2]/255
            ))
            
            # Handle custom message or default
            if self.settings['custom_message'].strip():
                message = self.settings['custom_message'].replace('{occasion}', occasion)
            else:
                message = f"You are warmly invited to our {occasion}."
            
            # Simple word wrapping for message
            max_width = self.settings['message_width'] * mm
            words = message.split()
            lines = []
            current_line = []
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                if c.stringWidth(test_line, "Helvetica", self.settings['message_font_size']) <= max_width:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]
            if current_line:
                lines.append(' '.join(current_line))
            
            # Draw message lines
            base_x = self.settings['message_x'] * mm
            base_y = self.settings['message_y'] * mm
            line_height = self.settings['message_font_size'] * 1.2
            
            for i, line in enumerate(lines):
                y_pos = base_y - (i * line_height)
                
                if self.settings['message_align'] == 'center':
                    text_width = c.stringWidth(line, "Helvetica", self.settings['message_font_size'])
                    x_pos = (width - text_width) / 2
                elif self.settings['message_align'] == 'right':
                    text_width = c.stringWidth(line, "Helvetica", self.settings['message_font_size'])
                    x_pos = width - text_width - base_x
                else:
                    x_pos = base_x
                
                c.drawString(x_pos, y_pos, line)
        
        # Event Details Zone
        if self.settings['show_event_details'] and self.settings['event_details'].strip():
            c.setFont("Helvetica", self.settings['details_font_size'])
            c.setFillColor(colors.Color(
                self.settings['details_color'][0]/255,
                self.settings['details_color'][1]/255,
                self.settings['details_color'][2]/255
            ))
            
            details = self.settings['event_details'].strip()
            detail_lines = details.split('\n')
            
            base_x = self.settings['details_x'] * mm
            base_y = self.settings['details_y'] * mm
            line_height = self.settings['details_font_size'] * 1.2
            
            for i, line in enumerate(detail_lines):
                y_pos = base_y - (i * line_height)
                
                if self.settings['details_align'] == 'center':
                    text_width = c.stringWidth(line, "Helvetica", self.settings['details_font_size'])
                    x_pos = (width - text_width) / 2
                elif self.settings['details_align'] == 'right':
                    text_width = c.stringWidth(line, "Helvetica", self.settings['details_font_size'])
                    x_pos = width - text_width - base_x
                else:
                    x_pos = base_x
                
                c.drawString(x_pos, y_pos, line)
        
        # RSVP Button Zone
        if self.settings['show_rsvp_button']:
            button_x = self.settings['button_x'] * mm
            button_y = self.settings['button_y'] * mm
            button_w = self.settings['button_width'] * mm
            button_h = self.settings['button_height'] * mm
            
            # Draw button background
            c.setFillColor(colors.Color(
                self.settings['button_bg_color'][0]/255,
                self.settings['button_bg_color'][1]/255,
                self.settings['button_bg_color'][2]/255
            ))
            c.rect(button_x, button_y, button_w, button_h, fill=1)
            
            # Button text
            c.setFillColor(colors.Color(
                self.settings['button_text_color'][0]/255,
                self.settings['button_text_color'][1]/255,
                self.settings['button_text_color'][2]/255
            ))
            c.setFont("Helvetica-Bold", self.settings['button_font_size'])
            
            button_text = self.settings['button_text']
            text_width = c.stringWidth(button_text, "Helvetica-Bold", self.settings['button_font_size'])
            text_x = button_x + (button_w - text_width) / 2
            text_y = button_y + (button_h - self.settings['button_font_size']) / 2
            
            c.drawString(text_x, text_y, button_text)
            
            # Add clickable link
            c.linkURL(link, (button_x, button_y, button_x + button_w, button_y + button_h))
        
        c.save()

class TemplatePreview(ctk.CTkToplevel):
    def __init__(self, parent, template_settings, template_image_path):
        super().__init__(parent)
        self.title("Template Preview")
        self.geometry("600x800")
        
        # Create preview (simplified - shows template zones)
        self.preview_frame = ctk.CTkFrame(self)
        self.preview_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        preview_text = f"""
Template Preview:
━━━━━━━━━━━━━━━━━━━━━━━━━━

Background: {'✓ Image Loaded' if template_image_path else '✗ No Image'}

Text Zones:
• Guest Name: {template_settings['name_x']}mm, {template_settings['name_y']}mm
• Main Message: {template_settings['message_x']}mm, {template_settings['message_y']}mm  
• Event Details: {template_settings['details_x']}mm, {template_settings['details_y']}mm
• RSVP Button: {template_settings['button_x']}mm, {template_settings['button_y']}mm

Font Sizes:
• Name: {template_settings['name_font_size']}pt
• Message: {template_settings['message_font_size']}pt
• Details: {template_settings['details_font_size']}pt
• Button: {template_settings['button_font_size']}pt
        """
        
        preview_label = ctk.CTkTextbox(self.preview_frame)
        preview_label.pack(fill="both", expand=True, padx=20, pady=20)
        preview_label.insert("1.0", preview_text)

class InviteApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Template-Based Invitation Generator")
        self.geometry("900x800")
        
        # Configure grid weight
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create main frame
        self.main_frame = ctk.CTkScrollableFrame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Initialize template settings
        self.template_settings = {
            # Guest name settings
            'show_guest_name': True,
            'name_x': 20,  # mm from left
            'name_y': 170, # mm from bottom
            'name_font_size': 14,
            'name_color': [0, 0, 0],
            'name_align': 'left',
            
            # Main message settings
            'show_main_message': True,
            'message_x': 20,
            'message_y': 150,
            'message_width': 108,  # max width in mm
            'message_font_size': 12,
            'message_color': [0, 0, 0],
            'message_align': 'left',
            'custom_message': '',
            
            # Event details settings
            'show_event_details': True,
            'details_x': 20,
            'details_y': 120,
            'details_font_size': 10,
            'details_color': [64, 64, 64],
            'details_align': 'left',
            'event_details': '',
            
            # RSVP button settings
            'show_rsvp_button': True,
            'button_x': 30,
            'button_y': 40,
            'button_width': 88,
            'button_height': 12,
            'button_bg_color': [0, 102, 204],
            'button_text_color': [255, 255, 255],
            'button_font_size': 11,
            'button_text': 'Click Here to RSVP'
        }
        
        self.selected_file = None
        self.template_image_path = None
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title = ctk.CTkLabel(
            self.main_frame,
            text="Template-Based Invitation Generator",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=(0, 20))
        
        # Template selection frame
        template_frame = ctk.CTkFrame(self.main_frame)
        template_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(template_frame, text="Step 1: Select Background Template", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 5))
        
        ctk.CTkLabel(template_frame, 
                    text="Upload your designed template (PNG, JPG) - A5 size (148×210mm) recommended",
                    font=ctk.CTkFont(size=12)).pack(pady=5)
        
        self.template_label = ctk.CTkLabel(template_frame, text="No template selected")
        self.template_label.pack(pady=5)
        
        template_buttons = ctk.CTkFrame(template_frame)
        template_buttons.pack(pady=10)
        
        self.template_button = ctk.CTkButton(
            template_buttons,
            text="Choose Template Image",
            command=self.choose_template,
            width=200,
            height=40
        )
        self.template_button.pack(side="left", padx=5)
        
        self.preview_button = ctk.CTkButton(
            template_buttons,
            text="Preview Template",
            command=self.preview_template,
            width=150,
            height=40,
            state="disabled"
        )
        self.preview_button.pack(side="left", padx=5)
        
        # Text positioning frame
        positioning_frame = ctk.CTkFrame(self.main_frame)
        positioning_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(positioning_frame, text="Step 2: Position Text Elements", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 5))
        
        self.create_positioning_controls(positioning_frame)
        
        # File selection frame
        file_frame = ctk.CTkFrame(self.main_frame)
        file_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(file_frame, text="Step 3: Select Guest Data", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 5))
        
        self.file_label = ctk.CTkLabel(file_frame, text="No Excel file selected")
        self.file_label.pack(pady=5)
        
        self.file_button = ctk.CTkButton(
            file_frame,
            text="Choose Excel File",
            command=self.choose_file,
            width=200,
            height=40
        )
        self.file_button.pack(pady=(5, 15))
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.main_frame)
        self.progress_bar.pack(fill="x", pady=(0, 10))
        self.progress_bar.set(0)
        
        # Generate button
        self.generate_button = ctk.CTkButton(
            self.main_frame,
            text="Generate Template-Based Invitations",
            command=self.generate_invites,
            width=350,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            state="disabled"
        )
        self.generate_button.pack(pady=20)
        
    def create_positioning_controls(self, parent):
        controls_frame = ctk.CTkFrame(parent)
        controls_frame.pack(fill="x", padx=10, pady=10)
        
        # Guest Name positioning
        name_frame = ctk.CTkFrame(controls_frame)
        name_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(name_frame, text="Guest Name Position", 
                    font=ctk.CTkFont(weight="bold")).pack(pady=(5, 0))
        
        name_controls = ctk.CTkFrame(name_frame)
        name_controls.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(name_controls, text="X (mm):").pack(side="left")
        self.name_x_var = ctk.StringVar(value=str(self.template_settings['name_x']))
        name_x_entry = ctk.CTkEntry(name_controls, textvariable=self.name_x_var, width=60)
        name_x_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(name_controls, text="Y (mm):").pack(side="left", padx=(20,0))
        self.name_y_var = ctk.StringVar(value=str(self.template_settings['name_y']))
        name_y_entry = ctk.CTkEntry(name_controls, textvariable=self.name_y_var, width=60)
        name_y_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(name_controls, text="Size:").pack(side="left", padx=(20,0))
        self.name_size_var = ctk.StringVar(value=str(self.template_settings['name_font_size']))
        name_size_entry = ctk.CTkEntry(name_controls, textvariable=self.name_size_var, width=60)
        name_size_entry.pack(side="left", padx=5)
        
        # Message positioning
        message_frame = ctk.CTkFrame(controls_frame)
        message_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(message_frame, text="Main Message Position", 
                    font=ctk.CTkFont(weight="bold")).pack(pady=(5, 0))
        
        message_controls = ctk.CTkFrame(message_frame)
        message_controls.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(message_controls, text="X (mm):").pack(side="left")
        self.message_x_var = ctk.StringVar(value=str(self.template_settings['message_x']))
        message_x_entry = ctk.CTkEntry(message_controls, textvariable=self.message_x_var, width=60)
        message_x_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(message_controls, text="Y (mm):").pack(side="left", padx=(20,0))
        self.message_y_var = ctk.StringVar(value=str(self.template_settings['message_y']))
        message_y_entry = ctk.CTkEntry(message_controls, textvariable=self.message_y_var, width=60)
        message_y_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(message_controls, text="Size:").pack(side="left", padx=(20,0))
        self.message_size_var = ctk.StringVar(value=str(self.template_settings['message_font_size']))
        message_size_entry = ctk.CTkEntry(message_controls, textvariable=self.message_size_var, width=60)
        message_size_entry.pack(side="left", padx=5)
        
        # Custom message
        self.custom_message_entry = ctk.CTkEntry(
            message_frame, 
            placeholder_text="Custom message (use {occasion} for event type)",
            width=400
        )
        self.custom_message_entry.pack(pady=5)
        
        # Event details positioning
        details_frame = ctk.CTkFrame(controls_frame)
        details_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(details_frame, text="Event Details Position", 
                    font=ctk.CTkFont(weight="bold")).pack(pady=(5, 0))
        
        details_controls = ctk.CTkFrame(details_frame)
        details_controls.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(details_controls, text="X (mm):").pack(side="left")
        self.details_x_var = ctk.StringVar(value=str(self.template_settings['details_x']))
        details_x_entry = ctk.CTkEntry(details_controls, textvariable=self.details_x_var, width=60)
        details_x_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(details_controls, text="Y (mm):").pack(side="left", padx=(20,0))
        self.details_y_var = ctk.StringVar(value=str(self.template_settings['details_y']))
        details_y_entry = ctk.CTkEntry(details_controls, textvariable=self.details_y_var, width=60)
        details_y_entry.pack(side="left", padx=5)
        
        self.details_text = ctk.CTkTextbox(details_frame, height=60)
        self.details_text.pack(fill="x", padx=10, pady=5)
        self.details_text.insert("1.0", "Date: [Date]\nTime: [Time]\nVenue: [Venue]\nDress Code: [Dress Code]")
        
        # Button positioning
        button_frame = ctk.CTkFrame(controls_frame)
        button_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(button_frame, text="RSVP Button Position", 
                    font=ctk.CTkFont(weight="bold")).pack(pady=(5, 0))
        
        button_controls = ctk.CTkFrame(button_frame)
        button_controls.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(button_controls, text="X (mm):").pack(side="left")
        self.button_x_var = ctk.StringVar(value=str(self.template_settings['button_x']))
        button_x_entry = ctk.CTkEntry(button_controls, textvariable=self.button_x_var, width=60)
        button_x_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(button_controls, text="Y (mm):").pack(side="left", padx=(20,0))
        self.button_y_var = ctk.StringVar(value=str(self.template_settings['button_y']))
        button_y_entry = ctk.CTkEntry(button_controls, textvariable=self.button_y_var, width=60)
        button_y_entry.pack(side="left", padx=5)
        
        self.button_text_entry = ctk.CTkEntry(
            button_frame,
            placeholder_text="Button Text",
            width=300
        )
        self.button_text_entry.pack(pady=5)
        self.button_text_entry.insert(0, self.template_settings['button_text'])
        
    def choose_template(self):
        file = filedialog.askopenfilename(
            title="Select Template Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff"),
                ("All files", "*.*")
            ]
        )
        
        if file:
            self.template_image_path = file
            filename = os.path.basename(file)
            self.template_label.configure(text=f"✓ {filename}")
            self.preview_button.configure(state="normal")
            self.check_ready_to_generate()
    
    def preview_template(self):
        self.update_template_settings()
        preview_window = TemplatePreview(self, self.template_settings, self.template_image_path)
        preview_window.focus()
    
    def update_template_settings(self):
        """Update template settings from UI controls"""
        try:
            self.template_settings['name_x'] = float(self.name_x_var.get())
            self.template_settings['name_y'] = float(self.name_y_var.get())
            self.template_settings['name_font_size'] = int(self.name_size_var.get())
            
            self.template_settings['message_x'] = float(self.message_x_var.get())
            self.template_settings['message_y'] = float(self.message_y_var.get())
            self.template_settings['message_font_size'] = int(self.message_size_var.get())
            self.template_settings['custom_message'] = self.custom_message_entry.get()
            
            self.template_settings['details_x'] = float(self.details_x_var.get())
            self.template_settings['details_y'] = float(self.details_y_var.get())
            self.template_settings['event_details'] = self.details_text.get("1.0", "end-1c")
            
            self.template_settings['button_x'] = float(self.button_x_var.get())
            self.template_settings['button_y'] = float(self.button_y_var.get())
            self.template_settings['button_text'] = self.button_text_entry.get()
        except ValueError:
            pass  # Ignore invalid values during typing
    
    def choose_file(self):
        file = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if file:
            try:
                # Validate file
                df = pd.read_excel(file)
                required_cols = {"Name", "Link", "Occasion"}
                
                if not required_cols.issubset(df.columns):
                    messagebox.showerror(
                        "Error", 
                        f"Excel file must contain columns: {', '.join(required_cols)}\n\n" +
                        f"Found columns: {', '.join(df.columns)}"
                    )
                    return
                
                self.selected_file = file
                filename = os.path.basename(file)
                self.file_label.configure(text=f"✓ {filename} ({len(df)} guests)")
                self.check_ready_to_generate()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read Excel file:\n{e}")
    
    def check_ready_to_generate(self):
        """Enable generate button only when both template and data are ready"""
        if self.template_image_path and self.selected_file:
            self.generate_button.configure(state="normal")
        else:
            self.generate_button.configure(state="disabled")
    
    def generate_invites(self):
        if not self.selected_file or not self.template_image_path:
            messagebox.showerror("Error", "Please select both template image and Excel file")
            return
        
        # Select output directory
        output_dir = filedialog.askdirectory(title="Select Output Folder")
        if not output_dir:
            return
        
        # Update template settings
        self.update_template_settings()
        
        # Start generation in separate thread
        self.generate_button.configure(state="disabled", text="Generating...")
        self.progress_bar.set(0)
        
        thread = threading.Thread(target=self.generate_pdfs, args=(output_dir,))
        thread.daemon = True
        thread.start()
    
    def generate_pdfs(self, output_dir):
        try:
            df = pd.read_excel(self.selected_file)
            total = len(df)
            
            for idx, (_, row) in enumerate(df.iterrows()):
                pdf = InvitePDF(self.template_settings, self.template_image_path)
                filename = os.path.join(output_dir, f"{row['Name'].replace(' ', '_')}_invite.pdf")
                pdf.create_invite(row["Name"], row["Link"], row["Occasion"], filename)
                
                # Update progress on main thread
                progress = (idx + 1) / total
                self.after(0, lambda p=progress: self.progress_bar.set(p))
            
            # Show completion message on main thread
            self.after(0, lambda: self.generation_complete(total))
            
        except Exception as e:
            # Show error on main thread
            self.after(0, lambda: messagebox.showerror("Error", f"Generation failed:\n{e}"))
            self.after(0, lambda: self.generate_button.configure(state="normal", text="Generate Template-Based Invitations"))
    
    def generation_complete(self, count):
        messagebox.showinfo("Success", f"Generated {count} template-based invitations successfully!")
        self.generate_button.configure(state="normal", text="Generate Template-Based Invitations")
        self.progress_bar.set(0)

if __name__ == "__main__":
    app = InviteApp()
    app.mainloop()
