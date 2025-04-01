 class ProgressBarEmbed {
    constructor(containerId, publicId, options = {}) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            console.error(`Container with ID ${containerId} not found`);
            return;
        }

        this.publicId = publicId;
        this.options = {
            theme: options.theme || 'dark', // 'dark' or 'light'
            showUpdates: options.showUpdates !== false,
            animate: options.animate !== false,
            width: options.width || '100%',
            height: options.height || 'auto'
        };

        this.initStyles();
        this.loadProgress();
    }

    initStyles() {
        const styleId = 'progress-embed-styles';
        if (document.getElementById(styleId)) return;

        const style = document.createElement('style');
        style.id = styleId;
        style.textContent = `
            .progress-embed-container {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                margin: 10px 0;
            }
            
            .progress-embed-dark {
                background-color: #1a202c;
                color: white;
            }
            
            .progress-embed-light {
                background-color: white;
                color: #2d3748;
                border: 1px solid #e2e8f0;
            }
            
            .progress-embed-header {
                padding: 12px 16px;
                font-weight: 600;
                font-size: 1.1rem;
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }
            
            .progress-embed-light .progress-embed-header {
                border-bottom-color: #e2e8f0;
            }
            
            .progress-embed-content {
                padding: 16px;
            }
            
            .progress-bar-container {
                width: 100%;
                height: 20px;
                background-color: rgba(255,255,255,0.1);
                border-radius: 10px;
                overflow: hidden;
                margin-bottom: 8px;
            }
            
            .progress-embed-light .progress-bar-container {
                background-color: #edf2f7;
            }
            
            .progress-bar {
                height: 100%;
                background-color: #48bb78;
                width: 0;
                transition: width 0.5s ease;
            }
            
            .progress-percentage {
                font-size: 0.9rem;
                text-align: center;
                margin-bottom: 12px;
            }
            
            .progress-updates {
                margin-top: 16px;
            }
            
            .progress-update {
                padding: 8px 0;
                border-bottom: 1px solid rgba(255,255,255,0.05);
            }
            
            .progress-embed-light .progress-update {
                border-bottom-color: #edf2f7;
            }
            
            .progress-update:last-child {
                border-bottom: none;
            }
            
            .progress-update-title {
                font-weight: 600;
                margin-bottom: 4px;
            }
            
            .progress-update-description {
                font-size: 0.85rem;
                opacity: 0.8;
            }
            
            .progress-update-date {
                font-size: 0.75rem;
                opacity: 0.6;
                margin-top: 4px;
            }
        `;
        document.head.appendChild(style);
    }

    async loadProgress() {
        try {
            const response = await fetch(`/api/progress/${this.publicId}/`);
            const data = await response.json();

            if (!data.success) {
                this.showError(data.error || 'Failed to load progress');
                return;
            }

            this.renderProgress(data);
        } catch (error) {
            this.showError('Failed to fetch progress data');
            console.error(error);
        }
    }

    renderProgress(data) {
        // Clear container
        this.container.innerHTML = '';

        // Create main container
        const mainDiv = document.createElement('div');
        mainDiv.className = `progress-embed-container progress-embed-${this.options.theme}`;
        mainDiv.style.width = this.options.width;

        // Add header
        const header = document.createElement('div');
        header.className = 'progress-embed-header';
        header.textContent = data.name;
        mainDiv.appendChild(header);

        // Add content
        const content = document.createElement('div');
        content.className = 'progress-embed-content';

        // Progress bar
        const barContainer = document.createElement('div');
        barContainer.className = 'progress-bar-container';

        const progressBar = document.createElement('div');
        progressBar.className = 'progress-bar';
        if (this.options.animate) {
            setTimeout(() => {
                progressBar.style.width = `${data.percentage}%`;
            }, 100);
        } else {
            progressBar.style.width = `${data.percentage}%`;
        }
        barContainer.appendChild(progressBar);
        content.appendChild(barContainer);

        // Percentage text
        const percentageText = document.createElement('div');
        percentageText.className = 'progress-percentage';
        percentageText.textContent = `${data.percentage}% completed`;
        content.appendChild(percentageText);

        // Updates if enabled
        if (this.options.showUpdates && data.updates && data.updates.length > 0) {
            const updatesContainer = document.createElement('div');
            updatesContainer.className = 'progress-updates';

            data.updates.forEach(update => {
                const updateDiv = document.createElement('div');
                updateDiv.className = 'progress-update';

                const title = document.createElement('div');
                title.className = 'progress-update-title';
                title.textContent = update.title;
                updateDiv.appendChild(title);

                if (update.description) {
                    const desc = document.createElement('div');
                    desc.className = 'progress-update-description';
                    desc.textContent = update.description;
                    updateDiv.appendChild(desc);
                }

                const date = document.createElement('div');
                date.className = 'progress-update-date';
                date.textContent = update.created_at;
                updateDiv.appendChild(date);

                updatesContainer.appendChild(updateDiv);
            });

            content.appendChild(updatesContainer);
        }

        mainDiv.appendChild(content);
        this.container.appendChild(mainDiv);
    }

    showError(message) {
        this.container.innerHTML = `
            <div style="padding: 10px; background: #fee2e2; color: #b91c1c; border-radius: 4px; font-size: 0.9rem;">
                Progress bar error: ${message}
            </div>
        `;
    }
}

// Auto-initialize if data attribute is present
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-progress-embed]').forEach(element => {
        const publicId = element.getAttribute('data-progress-embed');
        const options = {
            theme: element.getAttribute('data-theme') || 'dark',
            showUpdates: element.getAttribute('data-show-updates') !== 'false',
            animate: element.getAttribute('data-animate') !== 'false',
            width: element.getAttribute('data-width') || '100%'
        };

        new ProgressBarEmbed(element.id, publicId, options);
    });
});